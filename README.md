# PDF Word Count

A script for parsing pdf files and creating a simple database (Sqlite3) pdf_file | page | word | count. It simplifies searching for occurences of words in a large collection of pdf files (for ex. if you have a large collection of pdf magazines and want to find in which one a particular word has appeared).

## Getting Started

Clone the project from github:

```
git clone http://github.com/ultcyber/pdf_word_count
```

### Prerequisities

The script was written for Python 3.4.3.

Besides standard library modules (collections, re, sqlite3, os), you'll need argparse and PyPDF2

Either install the modules individually (using pip or easy_install) or use requirements.txt:
```
pip install -r requirements.txt
```

### Usage

Use command line to launch the script.

Positional (mandatory) argument:

path
	Path to the folder - type . to indicate current folder

Optional arguments:

-h, --help
	show usage and exit

-database 
	Path to the database file - if not provided, database.db is used as a default file and placed in cwd

-verbose
	Asks for every folder

-sverbose
	Asks for every file


Example:

```
python pdf_parser.py . -sverbose
```

Will walk the current working directory and ask for user input (yes/no) before parsing a file.


## Author

* **Mateusz Trybulec** - [Ultcyber](https://github.com/ultcyber)

## License

This project is licensed under the MIT License.

