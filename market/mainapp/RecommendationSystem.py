# from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
# from sklearn.neighbors import NearestNeighbors
# from sklearn.cluster import KMeans
# from sklearn.metrics import adjusted_rand_score
# import pandas as pd
# import matplotlib.pyplot as plt
# from .models import Product
#
# def train_model():
#     products = Product.objects.all()
#     product_description = products.values_list('Product_description', flat=True)
#     vectorizer = TfidfVectorizer(stop_words='english')
#     X1 = vectorizer.fit_transform(product_description)
#     kmeans = KMeans(n_clusters=10, init='k-means++')
#     kmeans.fit(X1)
#     return kmeans, vectorizer
#
# def print_cluster(terms, order_centroids, i):
#     print("Cluster %d:" % i),
#     for ind in order_centroids[i, :10]:
#         print(' %s' % terms[ind]),
#     print()
#
# def get_recommendations(product_name, kmeans, vectorizer):
#     Y = vectorizer.transform([product_name])
#     prediction = kmeans.predict(Y)
#     return prediction[0]
#
# def print_top_terms_per_cluster(kmeans, vectorizer):
#     true_k = 3
#     order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
#     terms = vectorizer.get_feature_names()
#     for i in range(true_k):
#         print_cluster(terms, order_centroids, i)
