import json
import pickle
from pprint import pprint
from deep_translator import GoogleTranslator
from os.path import exists

def transformer(bible_info_name:str) -> None:

    data = {}

    # Carregamos
    if exists("bible_info.json"):
        with open(
            "bible_info.json",
            'r'
        ) as f:
            original = json.load(f)
    else:
        return

    # Precisamos traduzir os nomes de Inglês para Português
    translater = GoogleTranslator(source='en', target='pt')
    already_translated = set()
    incorrectly_translated = {
        "Gênese": "Gênesis",
        "1Samuel": "1 Samuel",
        "2Samuel": "2 Samuel",
        "Cântico de Salomão": "Cânticos",
        "Danilo": "Daniel",
        "Marca": "Marcos",
        "Trabalho": "Jó",
        "John": "João",
        "James": "Tiago",
        "Revelação": "Apocalipse"
    }

    book_name_in_portuguese = None
    for element in original:
        # Traduzimos apenas uma vez, para obviamente não perdermos tempo
        if element["book"] not in already_translated:
            already_translated.add(element["book"])
            book_name_in_portuguese = translater.translate(element["book"])
            if book_name_in_portuguese in incorrectly_translated:
                book_name_in_portuguese = incorrectly_translated[book_name_in_portuguese]
            print(f"Traduzindo {element['book']} para {book_name_in_portuguese}")

        if book_name_in_portuguese not in data:
            data[book_name_in_portuguese] = []

        data[book_name_in_portuguese].append(element["verses"])

    for book_name in data:
        # O último elemento é a quantidade
        data[book_name].append(len(data[book_name]))

    final_name = "bible"
    with open(final_name + ".json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    with open(final_name + ".pkl", "wb") as f:
        pickle.dump(data, f)


if __name__ == '__main__':
    transformer("bible_info.json")
    # with open("result.pkl", "rb") as f:
    #     pprint(pickle.load(f))