import heapq

import Utils.normalizer as norm
import Utils.cleaner as cl
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from Utils.inverted_index import retrieve_relevant_document_IDs


def match(cleaned_corpus, corpus, inverted_index, query ):
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
    query_vector = vectorizerX.transform([q])

    print('query vector', query_vector)

    # calculate cosine similarities

    cosineSimilarities = cosine_similarity( query_vector, doc_vector,).flatten()
    # print('cos' , cosineSimilarities)

    relevant_documents_retrieved = [doc_index for doc_index in cosineSimilarities.argsort()[::-1] if
                                    cosineSimilarities[doc_index] > 0]
    # top_docs_indices = heapq.nlargest(10, range(len(cosineSimilarities)), cosineSimilarities.take)
    top_docs = [corpus[relevant_docs[i]] for i in relevant_documents_retrieved[0:10]]

    return top_docs



def match_clustring(corpus, relevant_docs, doc_vector, query, vectorizerX ):

    query_vector = vectorizerX.transform([query])

    print('query vector', query_vector)

    # calculate cosine similarities

    cosineSimilarities = cosine_similarity( query_vector, doc_vector,).flatten()
    # print('cos' , cosineSimilarities)

    relevant_documents_retrieved = [doc_index for doc_index in cosineSimilarities.argsort()[::-1] if
                                    cosineSimilarities[doc_index] > 0]


    # top_docs_indices = heapq.nlargest(10, range(len(cosineSimilarities)), cosineSimilarities.take)
    top_docs = [corpus[relevant_docs[i]] for i in relevant_documents_retrieved[0:10]]

    return top_docs