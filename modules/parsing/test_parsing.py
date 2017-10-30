from modules.parsing.parse_dictionary import *

if __name__ == "__main__":
    html_doc = read_document()
    dictionary = parse(html_doc,only_english=0)
    print(dictionary)
    write_data(dictionary)
