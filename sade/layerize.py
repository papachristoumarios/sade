import numpy as np
import networkx as nx
import sys
import pprint
import argparse
import collections
import pickle
import multiprocessing
import sade.community_detection
import sade.mdst


def bfs(G, s):
    depth = {}
    level = collections.defaultdict(list)
    q = collections.deque()
    for v in G.nodes():
        depth[v] = -1

    depth[s] = 0
    level[0] = [s]
    q.append(s)

    while q:
        u = q.popleft()

        for v in G[u]:
            if depth[v] == -1:
                depth[v] = depth[u] + 1
                q.append(v)
                level[depth[v]].append(v)

    return depth, level


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        description='Commnunity detection using the Louvain Algorithm')

    argparser.add_argument(
        '-e',
        type=str,
        help='Doc2Vec Embeddings',
        default='embeddings.bin')
    argparser.add_argument('-g', type=str, help='Call graph file')
    argparser.add_argument(
        '-d',
        type=int,
        help='Number of dimensions to reduce Embeddings Space',
        default=-1)
    args = argparser.parse_args()

    partition, communities, G, model = sade.community_detection.detect_communities(
        embeddings_filename=args.e, call_graph_file=args.g, dimensions=args.d)

    H = sade.community_detection.construct_induced_directed_graph(
        communities, partition, G)

    MDST = sade.mdst.mst(0, H)

    print(MDST)

    depth, level = bfs(MDST, 0)

    layers = collections.defaultdict(list)

    for lvl, _communities in level.items():
        for c in _communities:
            layers[lvl] = layers[lvl] + communities[c][0]

    pprint.pprint(layers)
