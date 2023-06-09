import re

from nltk import pos_tag
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
# from num2words import num2words

from Model.Country import names_dic
from Model.verbs import ir_verbs


def tokenize_lower(content):
    # tokenize and normalise a string.
    # set

    return [token.lower() for token in set(word_tokenize(content))]


def lower_words(words):
    # to lower case
    return [word.lower() for word in words]


def lower(word):
    # to lower case
    return word.lower()


def format_names(words):
    # formatting names
    nor_words = []
    for word in words:
        if word in names_dic:
            nor_words.append(names_dic[word])
        else:
            nor_words.append(word)

    return nor_words


def word_stemmer(token_list):
    ps = PorterStemmer()
    stemmed = []

    for word in token_list:
        stemmed.append(ps.stem(word))
    return stemmed


def normalize_words(words):
    # normalizing word
    nor_words = []
    # for word in words:
    # nor_words.append(stem_word(word))
    for tagged_word in pos_tag(words):
        tag = tagged_word[1]
        word = tagged_word[0]
        if tag.startswith("VB"):
            if irregular_verb(word):
                nor_words.append(stem_word(word))
            else:
                nor_words.append(WordNetLemmatizer().lemmatize(word, 'v'))
        else:
            nor_words.append(lem_word(word))

    return nor_words


def stem_words(words):
    # stemming words
    porter_stemmer = PorterStemmer()
    return [stem_word(w) for w in words]


def stem_word(word):
    # stemming word
    porter_stemmer = PorterStemmer()
    return porter_stemmer.stem(word)


def lem_words(words):
    # stemming word
    return [lem_word(w) for w in words]


def lem_word(word):
    # stemming word
    lemmatizer = WordNetLemmatizer()
    return lemmatizer.lemmatize(word)

#
# def numbers_to_words(words):
#     measurement = re.compile("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?")
#
#     _words = []
#
#     for word in words:
#         value = re.search(measurement, word)
#         if not value:
#             _words.append(word)
#         else:
#             value = value.group(0)
#             value = word.replace(value, num2words(int(value)))
#             _words.append(value)
#     return _words


def irregular_verb(word):
    return word in ir_verbs


