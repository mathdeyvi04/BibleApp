import requests
from urllib.parse import quote

def versiculo_pt(livro_en, cap, ver):
    url = f"https://bible-api.com/{livro_en} {cap}:{ver}?translation=almeida"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()["text"].strip()

print(versiculo_pt("Apocalipse", 1, 1))
