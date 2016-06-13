from collections import Counter
import re
import PyPDF2 as pdf
import sqlite3
import argparse
import os

class PDF_parser():
	def __init__(self, pathname, database_name):
		self.pathname = pathname
		self.database_name = database_name

	def __call__(self, list_filenames):
		self.list_filenames = list_filenames
		self.init_database(self.database_name)
		for fn in self.list_filenames:
			self.parse_pdf(fn)


	def init_database(self, database_name):
		# Connect to a database and create a table
		self.conn = sqlite3.connect(database_name)
		self.c = self.conn.cursor()
		self.c.execute("CREATE TABLE IF NOT EXISTS documents (id INTEGER PRIMARY KEY, name TEXT, page INTEGER, word TEXT, count INTEGER)")
		self.conn.commit()
		print("Database initialized!")

	def parse_pdf(self, pdf_file_name):

		with open(os.path.join(self.pathname, pdf_file_name), 'rb') as pdffile:
			
			pdf_wordbase = []
			
			try:
				pdfReader = pdf.PdfFileReader(pdffile)
				print("Analyzing " + pdf_file_name)
				numPages = pdfReader.numPages

				for page in range(1, numPages):
					current = pdfReader.getPage(page)
					text = current.extractText()
					wordbase = re.findall("[a-zA-z]+", text)
					
					for ind, word in enumerate(wordbase):
						wordbase[ind] = word.lower()
					
					wordbase = Counter(wordbase)
					pdf_wordbase.append(wordbase)
					print("Finished page {} for {}".format(str(page), str(numPages)))
					
					# Just for testing
					#if page == 20:
					#	break
					
					for word, count in wordbase.items():
						# Update table
						self.c.execute("INSERT INTO documents VALUES(NULL,?,?,?,?)", (pdf_file_name, page, word, count))

					# Commit to the database
					self.conn.commit()
			except:
				print("{} was not readable".format(pdf_file_name))
		

# Helper function
def ask(question):
	answer = input(question)
	if answer.lower() == "y" or answer.lower()=="yes":
		return True
	elif answer.lower() == "n" or answer.lower() == "no":
		return False
	else:
		print("Please type 'y(es)' or 'n(o)'")
		return ask(question)

# Main script

def main():
	# Parsing the arguments
	parser = argparse.ArgumentParser(description="PDF parser")
	parser.add_argument("path", help="Path to the folder - type . to indicate current folder")
	parser.add_argument("-database", dest="database", default="database.db", help="Path to the database file")
	parser.add_argument("-verbose", dest="verbose", action="store_true", default=False, help="Asks for every folder")
	parser.add_argument("-sverbose", dest="sverbose", action="store_true", default=False, help="Asks for every file")
	arguments = parser.parse_args()

	path = arguments.path

	# Checking whether the user forgot to specify flags
	if not arguments.verbose and not arguments.sverbose:
		if not ask("Do you really want {} and all it's subfolders to be analyzed? ".format(path)):
			print("Aborting...")
			quit()
	
	# Walking the directory tree. If there are any flags indicated, act accordingly
	for root, _, files in os.walk(path):
		# Skip files that are not pdf
		files = [file for file in files if re.search(".*\.pdf",file) != None]
		# If the folder does not contain any pdf files, print out a message and ignore
		if not files:
			print("{} does not contain any pdf files, skipping to next".format(root))
			continue
		
		if arguments.verbose and arguments.sverbose:
			if not ask("Do you want the {} folder to be analyzed? ".format(root)):
				print("Skipping " + root)
				continue
			parser = PDF_parser(root, arguments.database)
			for file in files:
				if not ask("Do you want {} to be analyzed? ".format(file)):
					print("Skipping " + file)
					continue
				parser([file])

		elif arguments.sverbose:
			parser = PDF_parser(root, arguments.database)
			for file in files:
				if re.search(".*\.pdf", file) != None:
					if not ask("Do you want {} to be analyzed? ".format(file)):
						print("Skipping " + file)
						continue
					parser([file])

		elif arguments.verbose:
			if not ask("Do you want the {} folder to be analyzed? ".format(root)):
				print("Skipping " + root)
				continue
			parser = PDF_parser(root, arguments.database)
			parser(files)
		
		else:
			parser = PDF_parser(root, arguments.database)
			parser(files)

	print("Done!")

if __name__ == '__main__':
	main()
