# Hierarchical Clustering for Document Embeddings
# usage: python3 clustering.py -h
# Author: Marios Papachristou

# Imports
import numpy as np
import networkx as nx
import pprint
from scipy import ndimage
from matplotlib import pyplot as plt
from sklearn import manifold
import gensim
import sade.mdst
import community
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

def generate_graph(call_graph_file, model):

    G = nx.DiGraph()

    with open(call_graph_file, 'r') as f:
        lines = f.read().splitlines()

    for line in lines:
        u, v = line.split()
        try:
            vu, vv = model.docvecs[u], model.docvecs[v]
            rho = get_corr_coeff(vu, vv)

            # Normalize
            rho_n = (1.0 + rho) / 2

            G.add_edge(u, v, weight=rho)

        except:
            pass

    return G

def get_communities(partition):
    communities = collections.defaultdict(list)

    for u, v in partition.items():
        communities[v].append(u)

    return communities

def get_mean_embeddings(communities, model=None):
    embeddings = {}

    for idx, files in communities.items():
        embeddings[idx] = (files, np.mean([model.docvecs[x] for x in files], axis=0))

    return embeddings

def construct_induced_graph(embeddings, partition, G, directed=True):
    if directed:
        H = nx.DiGraph()
    else:
        H = nx.Graph()

    # Construct non-weighted H
    for u, v in G.edges():
        pu, pv = partition[u], partition[v]
        if pu == pv:
            continue
        H.add_edge(pu, pv)

    for (u, v, w) in H.edges(data=True):
        # Compute rho
        uu, vv = embeddings[u][1], embeddings[v][1]

        rho = get_corr_coeff(uu, vv)
        rho_n = (1.0 - rho) / 2

        w['weight'] = rho_n

    print(H.edges(data=True))
    return H

def detect_communities(embeddings_filename, dimensions, call_graph_file):
        X, y, model = load_data(embeddings_filename)
        n_samples, n_features = X.shape

        # Reduce dimensions
        if dimensions != -1:
            X = manifold.SpectralEmbedding(n_components=dimensions).fit_transform(X)
            for doctag, vec in zip(model.docvecs.doctags, X):
                model.docvecs[doctag] = vec

        G = generate_graph(call_graph_file, model)

        partition = community.best_partition(nx.Graph(G))
        communities = get_communities(partition)
        embeddings = get_mean_embeddings(communities, model)

        pprint.pprint(communities)

        return partition, communities, embeddings, G, model

def detect_communities_helper(G, model):
        partition = community.best_partition(nx.Graph(G))
        communities = get_communities(partition)
        embeddings = get_mean_embeddings(communities, model)
        pprint.pprint(communities)
        return partition, communities, embeddings


if __name__ == '__main__':
    # Initialize
    argparser = argparse.ArgumentParser(description='Commnunity detection using the Louvain Algorithm')

    argparser.add_argument('-e', type=str, help='Doc2Vec Embeddings', default='embeddings.bin')
    argparser.add_argument('-g', type=str, help='Call graph file')
    argparser.add_argument('-d', type=int, help='Number of dimensions to reduce Embeddings Space', default=-1)

    args = argparser.parse_args()

    detect_communities(embeddings_filename=args.e, call_graph_file=args.g, dimensions=args.d)
