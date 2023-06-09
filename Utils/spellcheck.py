from __future__ import annotations

import enchant
from nltk.corpus import wordnet as wn


def spell_check(words):
    # checks the spelling mistakes for each word and returns suggestions.
    checker = enchant.DictWithPWL("en_US", "custom_dictionary.txt")
    error_dict = {}

    for w in words:

        if not checker.check(w):
            if w not in error_dict:
                error_dict[w] = checker.suggest(w)
    return error_dict


from textblob import TextBlob


def correct(text: str) -> str | None:
    corrected_text = str(TextBlob(text).correct())
    return corrected_text
