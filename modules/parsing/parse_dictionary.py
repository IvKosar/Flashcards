import os
import io
from zipfile import ZipFile
from bs4 import BeautifulSoup, SoupStrainer

BASE_DIR = os.environ.get("BASE_DIR")
OUT_PATH = os.environ.get("OUT_PATH")
ZIP_ARCHIVE = os.environ.get("ZIP_ARCHIVE")
FILENAME = os.environ.get("FILENAME")

def read_document():
    with ZipFile(BASE_DIR + 'modules/' + OUT_PATH + ZIP_ARCHIVE) as myzip:
        if not os.path.exists(OUT_PATH + FILENAME):
            myzip.extract(FILENAME, OUT_PATH)
        with myzip.open(FILENAME) as file:
            return file.read()

def parse(html_doc, only_english=1):
    languages = (3,2)
    table = SoupStrainer("tbody")
    soup = BeautifulSoup(html_doc, "html.parser", parse_only=table)

    line = soup.tr
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

    return dictionary


def write_data(dictionary):
    with open(BASE_DIR + 'modules/' + OUT_PATH + "cards.csv", 'w') as file:
        for key in dictionary:
            line = key + ";" + dictionary[key] + '\n'
            file.write(line)
