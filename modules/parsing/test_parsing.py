from modules.parsing.parse_dictionary import *

if __name__ == "__main__":
    html_doc = read_zip_archive()
    last_row_num = get_last_row_num()
    dictionary = parse(html_doc, last_row_num,only_english=0)
    print(len(dictionary))
    #write_data(dictionary)
    #read_document("/media/ivan/2AC2E2F12DC00F2B/Ivan/Documents/Programming/Simple programs/Flashcards/modules/data/input")
