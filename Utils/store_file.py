import json


def store_cleaned_corpus(file ,cleaned_corpus):
    with open(file ,'w', encoding="utf-8") as file:
        json.dump(cleaned_corpus, file)


def read_cleaned_corpus(file):
    with open(file, 'r' ,encoding="utf-8") as file:
        cleaned_corpus = json.load(file)
        return cleaned_corpus