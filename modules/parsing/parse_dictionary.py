import os
import io
from zipfile import ZipFile
from bs4 import BeautifulSoup, SoupStrainer

BASE_DIR = os.environ.get("BASE_DIR")
OUT_PATH = os.environ.get("OUT_PATH")
ZIP_ARCHIVE = os.environ.get("ZIP_ARCHIVE")
FILENAME = os.environ.get("FILENAME")
DATA_DIR = os.environ.get("DATA_DIR")

def read_zip_archive():
    with ZipFile(BASE_DIR + OUT_PATH + ZIP_ARCHIVE) as myzip:
        if not os.path.exists(OUT_PATH + FILENAME):
            myzip.extract(FILENAME, OUT_PATH)
        with myzip.open(FILENAME) as file:
            return file.read()

def read_document(filename):
    with open(filename) as infile:
        outfile = open(BASE_DIR + OUT_PATH + 'cards.csv', 'a')
        for line in infile.readlines():
            if line:
                new_line = line.strip().split()
                n = len(new_line)
                german = new_line[0].lower() + ' ' + new_line[1]
                ukrainian = new_line[-1] if n  == 3 else ' '.join(new_line[-2:])
                outfile.write(german + ';' + ukrainian + '\n')
        outfile.close()


def get_last_row_num():
    with open(BASE_DIR + DATA_DIR + 'last_row') as file:
        try:
            return int(file.read())
        except ValueError:
            print("Wrong data in file with last row number")

def parse(html_doc, last_row_num,only_english=1):
    table = SoupStrainer("tbody")
    soup = BeautifulSoup(html_doc, "html.parser", parse_only=table)

    # go through lines until reach the first non added to dictionary
    line = soup.tr
    count = 0
    while count < last_row_num:
        line = line.next_sibling
        count += 1

    # parse the row for german and english or ukrainian words
    dictionary = {}
    while line.next_sibling:
        line = line.next_sibling
        if only_english:
            cell_1, cell_2 = list(line.children)[:2]
        else:
            cell_1, cell_2 = list(line.children)[0], list(line.children)[2]
        german = cell_1.get_text()
        other = cell_2.get_text()
        if not german:
            continue
        dictionary[german] = other

        count += 1

    with open(BASE_DIR + DATA_DIR + "last_row", 'w') as file:
        file.write(str(count))

    return dictionary


def write_data(dictionary):
    with open(BASE_DIR + OUT_PATH + "cards.csv", 'w') as file:
        for key in dictionary:
            line = key + ";" + dictionary[key] + '\n'
            file.write(line)
