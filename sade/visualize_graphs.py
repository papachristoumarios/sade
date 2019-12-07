import networkx as nx
import numpy as np
import argparse
import json
import matplotlib.pyplot as plt
from gensim.models import Doc2Vec
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.manifold import SpectralEmbedding
from sade.community_detection import load_data, generate_graph

def load_clusters(bunch_file):
    with open(bunch_file) as f:
        lines = f.read().splitlines()

    clusters = {}
    for line in lines:
        name, files = line.split('= ')
        try:
            name = int(name)
        except:
            pass

        files = files.split(', ')

        for filename in files:
            clusters[filename] = name

    return clusters

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-g', help='Input graph')
    argparser.add_argument('-e', help='Doc2vec model')
    argparser.add_argument('-m', help='Modules file')
    argparser.add_argument('-b', help='Bunchfile')
    argparser.add_argument('--method', default='tsne', help='Method for dim reduction')
    args = argparser.parse_args()

    if args.method == 'pca':
        clf = PCA(n_components=2)
    elif args.method == 'tsne':
        clf = TSNE(n_components=2)
    elif args.method == 'spectral':
        clf = SpectralEmbedding(n_components=2)

    modules = json.load(open(args.m))

    X, y, model = load_data(args.e)

    X_ = clf.fit_transform(X)

    G = generate_graph(args.g, model, modules)

    pos_n = dict(zip(y, map(lambda x: x.tolist(), X_)))


    plt.figure()
    

    if args.b == None:
        nx.draw_networkx_edges(G, pos_n, nodelist=G.nodes(), alpha=0.2)
        nx.draw_networkx_nodes(G, pos_n, nodelist=G.nodes(),
                           node_size=40,
                           alpha=0.6,
                           cmap=plt.cm.Reds_r)
    else:
        clusters = load_clusters(args.b)
        # import pdb; pdb.set_trace()
        nx.draw_networkx_edges(G, pos_n, nodelist=list(clusters.keys()), alpha=0.4, cmap=plt.cm.Blues_r)
        nx.draw_networkx_nodes(G, pos_n, nodelist=list(clusters.keys()),
                           node_size=40,
                           node_color=(list(clusters.values())),
                           alpha=0.9,
                           cmap=plt.cm.Reds_r)


    plt.axis('off')
    plt.show()
