from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import pandas as pd
import matplotlib.pyplot as plt
from .models import Product
product_file=Product.objects.values_list('Product_description','Product_asin','id')
product=pd.DataFrame(product_file,columns=['Product_description','Product_asin','Product_id'])
product_description = product['Product_description']
def train():
    vectorizer = TfidfVectorizer(stop_words='english')
    X1 = vectorizer.fit_transform(product_description)
    X=X1
    kmeans = KMeans(n_clusters = 10, init = 'k-means++')
    y_kmeans = kmeans.fit_predict(X)
    true_k = 3
    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
    model.fit(X1)
    print("Top terms per cluster:")
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    return vectorizer,model,order_centroids,terms
def print_cluster(i):
    vectorizer,model,order_centroids,terms =train()
    print("Cluster %d:" % i),
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind]),
    print
# def show_recommendations(product):
#     #print("Cluster ID:")
#     Y = vectorizer.transform([product])
#     prediction = model.predict(Y)
#     #print(prediction)
#     print_cluster(prediction[0])

def show_recommendations1(product_description):
        vectorizer,model,order_centroids,terms =train()
        print("product", product)
        print("product_description:",product_description)
        Y = vectorizer.transform([product_description])
        prediction = model.predict(Y)
        cluster_id = prediction[0]
        cluster_products = []
        for i, desc in enumerate(product_description):
            Y = vectorizer.transform([desc])
            pred = model.predict(Y)
            if pred[0] == cluster_id:
                cluster_products.append(product.iloc[i]['Product_asin'])
        def get_cluster_products(product_df, cluster_id):
                cluster_products = []
                for i, row in product_df.iterrows():
                    Y = vectorizer.transform([row['Product_description']])
                    prediction = model.predict(Y)
                    if prediction[0] == cluster_id:
                        cluster_products.append(row['Product_asin'])
                return cluster_products
        listOfProducts=get_cluster_products(product,)
        print("Cluster ID:", cluster_id)
        print("Products in this cluster:", cluster_products)
        return cluster_id,cluster_products

vectorizer,model,order_centroids,terms =train()
def show_recommendations(product_description):
    #print("Cluster ID:")
    Y = vectorizer.transform([product_description])
    prediction = model.predict(Y)
    #print(prediction)
    def get_cluster_products(product_df, cluster_id):
        cluster_products = []
        for i, row in product_df.iterrows():
            Y = vectorizer.transform([row['Product_description']])
            prediction = model.predict(Y)
            if prediction[0] == cluster_id:
                cluster_products.append(row['Product_asin'])
        return cluster_products
    recommedationProducts=get_cluster_products(product,prediction[0])
    print_cluster(prediction[0]) 
    return prediction[0],recommedationProducts
