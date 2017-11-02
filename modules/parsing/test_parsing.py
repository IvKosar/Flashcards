from modules.parsing.parse_dictionary import *

if __name__ == "__main__":
    html_doc = read_zip_archive()
    dictionary = parse(html_doc,only_english=0)
    #print(dictionary)
    write_data(dictionary)
    read_document("/media/ivan/2AC2E2F12DC00F2B/Ivan/Documents/Programming/Simple programs/Flashcards/modules/data/input")
