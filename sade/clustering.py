# Hierarchical Clustering for Document Embeddings
# usage: python3 clustering.py -h
# Author: Marios Papachristou

# Imports
import numpy as np
from scipy import ndimage
from matplotlib import pyplot as plt
from sklearn import manifold, datasets
import gensim
import gensim.models
from sklearn.cluster import AgglomerativeClustering
import collections
import argparse

np.random.seed(0)

# Compute cosine similarity
def get_corr_coeff(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

# Load data from doc2vec model
def load_data(embeddings_filename='embeddings.bin'):
    model = gensim.models.Doc2Vec.load(embeddings_filename)
    y = list(model.docvecs.doctags)
    X = []
    for x in y:
        X.append(model.docvecs[x])
    X = np.array(X)

    return X, y, model

# Plot clustering
def plot_clustering(X_red, labels, title=None):
    x_min, x_max = np.min(X_red, axis=0), np.max(X_red, axis=0)
    X_red = (X_red - x_min) / (x_max - x_min)

    plt.figure(figsize=(6, 4))
    for i in range(X_red.shape[0]):
        plt.text(X_red[i, 0], X_red[i, 1], str(y[i]),
                 color=plt.cm.nipy_spectral(labels[i] / 10.),
                 fontdict={'weight': 'bold', 'size': 9})

    plt.xticks([])
    plt.yticks([])
    if title is not None:
        plt.title(title, size=17)
    plt.axis('off')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Compute Minimum Correlation in Clusters
def compute_score(X, labels, y, model):
    groups = collections.defaultdict(list)

    for i, label in enumerate(labels):
        groups[label].append((i, y[i]))

    correlations = {}
    for g in groups:
        correlations[g] = 2
        for i, yi in groups[g]:
            u = X[i]
            for j, yj in groups[g]:
                v = X[j]
                c = get_corr_coeff(u, v)
                correlations[g] = min(c, correlations[g])

    print(correlations)


    return min(correlations.values())


if __name__ == '__main__':
    # Initialize
    argparser = argparse.ArgumentParser(description='Hierarchical Clustering from embeddings')

    argparser.add_argument('-e', type=str, help='Doc2Vec Embeddings', default='embeddings.bin')
    argparser.add_argument('-d', type=int, help='Number of dimensions to reduce Embeddings Space', default=-1)
    argparser.add_argument('-n', type=int, help='Number of clusters', default=10)
    argparser.add_argument('-l', type=str, help='Linkage Type', default='ward')

    args = argparser.parse_args()

    X, y, model = load_data(args.e)
    n_samples, n_features = X.shape

    # Reduce dimensions
    if args.d != -1:
        X = manifold.SpectralEmbedding(n_components=2).fit_transform(X)

    linkage = args.l

    # Compute clustering with sklearn
    clustering = AgglomerativeClustering(linkage=linkage, n_clusters=args.n)
    clustering.fit(X)
    print('Linkage: {}'.format(linkage))
    if args.d in [1, 2, 3]:
        plot_clustering(X, clustering.labels_, "Linkage: {}".format(linkage).title())
    score_red = compute_score(X, clustering.labels_, y, model)
    print('Score: {}'.format(score_red))

    plt.show()
