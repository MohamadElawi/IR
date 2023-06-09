import re
import string

from nltk.corpus import stopwords


def remove_stop_words(words):
    stop_words = stopwords.words('english')
    return [w for w in words if w not in stop_words]


def remove_punctuation(words):
    exclude = set(string.punctuation)
    clean_word = []
    for word in words:
        clean_word.append(''.join(ch for ch in word if ch not in exclude))
    return clean_word


def replace_symbols(content):
    return re.sub("-|]|\[|\)|\(", ' ', content)


def remove_white_spaces(content):
    return re.sub(re.compile(r'\s+'), ' ', content)
