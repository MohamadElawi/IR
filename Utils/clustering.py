from sklearn.cluster import KMeans
import Utils.normalizer as norm
import Utils.cleaner as cl


def create_clusters(doc_vector):
    num_clusters = 10
    model = KMeans(n_clusters=num_clusters, init='k-means++', max_iter=100, n_init=1)
    model.fit(doc_vector)
    return model


def top_term_per_cluster(model, vectorizerX):
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizerX.get_feature_names_out()
    for i in range(10):
        print("Cluster %d:" % i),
        for ind in order_centroids[i, :10]:
            print(' %s' % terms[ind]),

    print(order_centroids)


def predict_cluster(vectorizerX, model, query):
    Y = vectorizerX.transform(query)
    prediction = model.predict(Y)
    return prediction
