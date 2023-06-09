import json
from collections import defaultdict
import Utils.normalizer as norm
import Utils.cleaner as cl
import Utils.spellcheck as sc
import datefinder

def build_inverted_index(dataset):
    inverted_index = defaultdict(list)
    for document in dataset:
            doc = cl.replace_symbols(document.content)
            doc = cl.remove_white_spaces(doc)
            tokens = norm.tokenize_lower(doc)
            doc_text = cl.remove_stop_words(tokens)
            doc_text = cl.remove_punctuation(doc_text)
            doc_text = norm.normalize_words(doc_text)
            doc_text = norm.format_names(doc_text)
            for token in doc_text:
                 inverted_index[token].append(document.id)
    return inverted_index


# Store the inverted index in a file
def store_inverted_index(file ,inverted_index):
    with open(file,'w', encoding="utf-8") as file:
        json.dump(inverted_index, file)

# Read the inverted index from the file
def read_inverted_index(file):
    with open(file, 'r' ,encoding="utf-8") as file:
        inverted_index = json.load(file)
        return inverted_index


def retrieve_relevant_document_IDs(inverted_index, query_tokens):
    relevant_docs = set()
    # Retrieve relevant document IDs using the inverted index
    for token in query_tokens:
        if token in inverted_index:
            relevant_docs.update(inverted_index[token])

    # Convert relevant document IDs to a list
    relevant_docs = list(relevant_docs)
    return relevant_docs