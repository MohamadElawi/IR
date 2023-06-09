from sklearn.feature_extraction.text import TfidfVectorizer

import Utils.normalizer as norm
import Utils.cleaner as cl
import Utils.spellcheck as sc
import datefinder
from Utils.clustering import create_clusters, predict_cluster, top_term_per_cluster
from Utils.inverted_index import build_inverted_index, store_inverted_index, read_inverted_index, \
    retrieve_relevant_document_IDs
from Utils.measurement import measure
from Utils.parser import parse_train_data, parse_test_data, parse_relevant_dic
from Utils.search import match, match_clustring
from Utils.store_file import store_cleaned_corpus, read_cleaned_corpus
from flask import Flask, render_template, request, jsonify


all_antique = parse_train_data()
queries = parse_test_data()
relevant_dic =parse_relevant_dic()
print('read all data')
#########################################################################

#### inverted_index = build_inverted_index(all_antique)
#### store_inverted_index('Files/result.tsv' ,inverted_index )
inverted_index =read_inverted_index('Files/result.tsv')
print('created inverted index')

corpus = {}
test_corpus = {}

for antique in all_antique:
     corpus[antique.id] = antique.content

for query in queries:
    test_corpus[query.id] = query.content


cleaned_corpus = {}
# for doc_id in corpus:
#     doc = corpus[doc_id]
#     doc = cl.replace_symbols(doc)
#     doc = cl.remove_white_spaces(doc)
#     tokens = norm.tokenize_lower(doc)
#     doc_text = cl.remove_stop_words(tokens)
#     doc_text = cl.remove_punctuation(doc_text)
#     doc_text = norm.normalize_words(doc_text)
#     doc_text = norm.format_names(doc_text)
#     doc_text = ' '.join(doc_text)
#     cleaned_corpus[doc_id] = doc_text

#### store_cleaned_corpus('Files/cleaned-corpus.tsv', cleaned_corpus)
cleaned_corpus =read_cleaned_corpus('Files/cleaned-corpus.tsv')
print('read clean corpos')

cleaned_test_corpus = {}
# for doc_id in test_corpus:
#     doc = test_corpus[doc_id]
#     doc = cl.replace_symbols(doc)
#     doc = cl.remove_white_spaces(doc)
#     tokens = norm.tokenize_lower(doc)
#     doc_text = cl.remove_stop_words(tokens)
#     doc_text = cl.remove_punctuation(doc_text)
#     doc_text = norm.normalize_words(doc_text)
#     doc_text = norm.format_names(doc_text)
#     doc_text = ' '.join(doc_text)
#     cleaned_test_corpus[int(doc_id)] = doc_text

######## store_cleaned_corpus('Files/cleaned-test-corpus.tsv', cleaned_test_corpus)
cleaned_test_corpus =read_cleaned_corpus('Files/cleaned-test-corpus.tsv')

# print(cleaned_test_corpus)


# vectorizerX.fit(cleaned_corpus)

# doc_vector = vectorizerX.fit_transform(cleaned_corpus)

# print(doc_vector.shape)




query = input('input your query\n')

relevant_documents_retrieved = match(cleaned_corpus, corpus, inverted_index, query)

for doc in relevant_documents_retrieved:
    print(doc)


measure(cleaned_corpus, cleaned_test_corpus, inverted_index, relevant_dic)



query = cl.replace_symbols(query)
query = cl.remove_white_spaces(query)
query = norm.tokenize_lower(query)
query = cl.remove_stop_words(query)
query = cl.remove_punctuation(query)
query = norm.format_names(query)
query_tokens = []
for w in norm.normalize_words(query):
    query_tokens.append(w)
q = ' '.join(query_tokens)
print('query', query_tokens)

relevant_docs = retrieve_relevant_document_IDs(inverted_index, query_tokens)
print('relevant doc', len(relevant_docs))

# Preprocess the relevant documents
preprocessed_docs = []
for doc_id in relevant_docs:
    preprocessed_docs.append(cleaned_corpus[doc_id])


vectorizerX = TfidfVectorizer()
doc_vector = vectorizerX.fit_transform(preprocessed_docs)


# building 10 clusters
model = create_clusters(doc_vector)

# print top term for each cluster
# top_term_per_cluster(model, vectorizerX)

# predicting relevant cluster
prediction = predict_cluster(vectorizerX, model, query)

cluster_corpus = []

for i , lable in enumerate(model.labels_):
    if lable in prediction:
        cluster_corpus.append(preprocessed_docs[i])

vectorizerZ = TfidfVectorizer()
vectorizerZ.fit(cluster_corpus)
doc_vector = vectorizerZ.transform(cluster_corpus)


relevant_documents_retrieved = match_clustring(corpus, relevant_docs, doc_vector, q, vectorizerZ)

print(len(relevant_documents_retrieved))
for doc in relevant_documents_retrieved:
    print(doc)

