from collections import Counter
import re
import PyPDF2 as pdf
import sqlite3

class PDF_parser():
	def __init__(self, pathname = "null"):
		self.pathname = pathname

	def __call__(self, list_filenames):
		self.list_filenames = list_filenames
		self.init_database()
		for fn in self.list_filenames:
			self.parse_pdf(fn)


	def init_database(self):
		# Connect to a database and create a table
		self.conn = sqlite3.connect('test.db')
		self.c = self.conn.cursor()
		self.c.execute("CREATE TABLE IF NOT EXISTS documents (id INTEGER PRIMARY KEY, name TEXT, page INTEGER, word TEXT, count INTEGER)")
		self.conn.commit()
		print("Database initialized!")

	def parse_pdf(self, pdf_file_name):

		with open(pdf_file_name, 'rb') as pdffile:
			
			pdf_wordbase = []
			
			pdfReader = pdf.PdfFileReader(pdffile)
			numPages = pdfReader.numPages

			for page in range(1, numPages):
				current = pdfReader.getPage(page)
				text = current.extractText()
				wordbase = re.findall("[a-zA-z]+", text)
				
				for ind, word in enumerate(wordbase):
					wordbase[ind] = word.lower()
				
				wordbase = Counter(wordbase)
				pdf_wordbase.append(wordbase)
				print("Finished page " + str(page))
				if page == 20:
					break
				
				for word, count in wordbase.items():
					# Update table
					self.c.execute("INSERT INTO documents VALUES(NULL,?,?,?,?)", (pdf_file_name, page, word, count))

				# Commit to the database
				self.conn.commit()

# Calls for test purposes
magazine = PDF_parser()
magazine(['linux-voice.pdf'])

# TODO:
# 1. Create an argument parser function that will:
# 	1.1 If no arguments provided, the program will just display "Type --help for help"
# 	1.2 Create a --path flag that will point to the target path
#	1.3 Create a --database flag that will point to the target database path, if not provided, database.db is used
# 	1.2 Create an --all flag that will just parse through all the subfolders in the target path without asking
# 	1.3 Create a --verbose flag that will ask user each time if it needs to parse a given subfolder in the folder
# 2. Wrap the pdf parsing in a try/except clause to make sure the files are read
# 3. Display a little report at the end to the console (how many files, which files were not readable)
