# Hierarchical Clustering for Document Embeddings
# usage: python3 clustering.py -h
# Author: Marios Papachristou

# Imports
import numpy as np
from scipy import ndimage
import os
if not os.environ.get('DISPLAY') is None:
    HEADLESS = False
    from matplotlib import pyplot as plt
else:
    HEADLESS = True

from sklearn import manifold
import gensim
import gensim.models
from sklearn.cluster import AgglomerativeClustering
import collections
import argparse
from sade.helpers import load_data, generate_bunch

np.random.seed(0)

# Compute cosine similarity


def get_corr_coeff(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))


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

    for key, val in groups.items():
        groups[key] = [elem[1] for elem in val]

    return groups, min(correlations.values())


if __name__ == '__main__':
    # Initialize
    argparser = argparse.ArgumentParser(
        description='Hierarchical Clustering from embeddings')

    argparser.add_argument(
        '-e',
        type=str,
        help='Doc2Vec Embeddings',
        default='embeddings.bin')
    argparser.add_argument(
        '-d',
        type=int,
        help='Number of dimensions to reduce Embeddings Space',
        default=-1)
    argparser.add_argument(
        '-n',
        type=int,
        help='Number of clusters',
        default=10)

    argparser.add_argument(
        '--stats',
        action='store_true',
        help='Print statistics on clusterings'
    )
    argparser.add_argument('-l', type=str, help='Linkage Type', default='ward')

    argparser.add_argument(
        '--affinity',
        type=str,
        default='euclidean',
        help='Affinity of linkage'
    )

    args = argparser.parse_args()

    X, y, model = load_data(args.e)
    n_samples, n_features = X.shape

    # Reduce dimensions
    if args.d != -1:
        X = manifold.SpectralEmbedding(n_components=args.d).fit_transform(X)

    linkage = args.l

    # Compute clustering with sklearn
    clustering = AgglomerativeClustering(linkage=linkage, n_clusters=args.n, affinity=args.affinity)
    clustering.fit(X)
    if args.d in [1, 2, 3] and not HEADLESS:
        plot_clustering(
            X,
            clustering.labels_,
            "Linkage: {}".format(linkage).title())
    groups, score_red = compute_score(X, clustering.labels_, y, model)
    generate_bunch(groups)

    if args.stats:
        print('Linkage: {}'.format(linkage))
        print('Score: {}'.format(score_red))
        print('Largest cluster size: ', max([len(z) for z in groups.values()]))
        print('Smallest cluster size: ', min([len(z) for z in groups.values()]))
        print('Mean cluster size: ', len(X) / args.n )
        print('Total modules', len(X))

    if not HEADLESS:
        plt.show()
