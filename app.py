from sklearn.feature_extraction.text import TfidfVectorizer

import Utils.normalizer as norm
import Utils.cleaner as cl
import Utils.spellcheck as sc
from Utils.clustering import create_clusters, predict_cluster
from Utils.inverted_index import build_inverted_index, store_inverted_index, read_inverted_index, \
    retrieve_relevant_document_IDs
from Utils.measurement import measure
from Utils.parser import parse_train_data, parse_test_data, parse_relevant_dic
from Utils.search import match, match_clustring
from Utils.store_file import store_cleaned_corpus, read_cleaned_corpus
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

all_antique = parse_train_data()

queries = parse_test_data()

relevant_dic =parse_relevant_dic()
print('read all data')

inverted_index = read_inverted_index('Files/result.tsv')
print('created inverted index')

corpus = {}
test_corpus = {}

for antique in all_antique:
     corpus[antique.id] = antique.content

for query in queries:
    test_corpus[query.id] = query.content


cleaned_corpus = {}
cleaned_corpus = read_cleaned_corpus('Files/cleaned-corpus.tsv')
print('read clean corpos')

cleaned_test_corpus = {}
cleaned_test_corpus = read_cleaned_corpus('Files/cleaned-test-corpus.tsv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cluster-search')
def cluster_index():
    return render_template('cluster-index.html')

@app.route('/query', methods=['POST'])
def process_query():
    query = request.form['query']
    query = sc.correct(query)
    relevant_documents_retrieved = match(cleaned_corpus, corpus, inverted_index, query)
    return jsonify(relevant_documents_retrieved=relevant_documents_retrieved)


@app.route('/cluster-query', methods=['POST'])
def cluster_process_query():
    query = request.form['query']
    query = sc.correct(query)
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


    # predicting relevant cluster
    prediction = predict_cluster(vectorizerX, model, query)

    cluster_corpus = []
    for i, lable in enumerate(model.labels_):
        if lable in prediction:
            cluster_corpus.append(preprocessed_docs[i])

    vectorizerZ = TfidfVectorizer()
    vectorizerZ.fit(cluster_corpus)
    doc_vector = vectorizerZ.transform(cluster_corpus)
    relevant_documents_retrieved = match_clustring(corpus, relevant_docs, doc_vector, q, vectorizerZ)
    return jsonify(relevant_documents_retrieved=relevant_documents_retrieved)

if __name__ == '__main__':
    app.run(debug=True)

exit()


