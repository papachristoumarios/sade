# Layerization Module
# Author: Marios Papachristou
import sys
import pprint
import argparse
import collections
import pickle
import numpy as np
import networkx as nx
import multiprocessing
import sade.community_detection
import sade.mdst
import sade.helpers


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

def layerize_mdst(embeddings_filename, dimensions, call_graph_file, modules_json, directed, visualize):
        partition, communities, embeddings, G, model, H = sade.community_detection.detect_communities(
            embeddings_filename=embeddings_filename, modules_json=modules_json, call_graph_file=call_graph_file, dimensions=dimensions, directed=directed, visualize=visualize)
        s = list(H.nodes())[0]
        print('s = ', str(s))
        MDST = sade.mdst.mst(H, s)
#        import pdb; pdb.set_trace()

        depth, layers = bfs(MDST, s)
       
        return layers

def is_path(G):
    r = list(G.nodes())[0]
    visited = collections.defaultdict(bool)
    visited[r] = True
    q = collections.deque([r])
    while q:
        u = q.popleft()
        for v in G[u]:
            if visited[v] == False:
                visited[v] = True
                q.append(v)
        if len(q) > 1:
            return False

    return True

def layerize_iterative(embeddings_filename, dimensions, call_graph_file, max_iter=10e6):
    # TODO finish
    print('Iteration 0')

    partition, communities, embeddings, G, model = sade.community_detection.detect_communities(
        embeddings_filename=embeddings_filename, call_graph_file=call_graph_file, dimensions=dimensions)

    if is_path(G):
        pprint.pprint(communities)
        return G, communities

    i = 1
    while (not is_path(G)) and (i <= max_iter) and (len(communities.keys()) > 1):
        print('Iteration ', i)
        G = sade.community_detection.construct_induced_graph(
            embeddings, partition, G, directed=False)
        partition, communities, embdddings = sade.community_detection.detect_communities_helper(G, model)

        i += 1


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
    argparser.add_argument('--type', type=str, help='Type of layerization', default='mdst')
    argparser.add_argument('--export', type=str, help='Export Type (json or bunch)', default='bunch')
    argparser.add_argument('--visualize', action='store_true', help='Generate dot files with GraphViz')
    argparser.add_argument('--directed', action='store_true', help='Assume edge directionality')
    argparser.add_argument('-m', type=str, help='Module definition file', default='')

    args = argparser.parse_args()

    if args.type == 'iterative':
        layers = layerize_iterative(embeddings_filename=args.e, dimensions=args.d, call_graph_file=args.g)
    elif args.type == 'mdst':
        layers = layerize_mdst(embeddings_filename=args.e, modules_json=args.m, dimensions=args.d, call_graph_file=args.g, directed=args.directed, visualize=args.visualize)

    if args.export == 'json':
        print(json.dumps(layers, indent=4, separators=(',', ': ')))
    elif args.export == 'bunch':
        print(sade.helpers.generate_bunch(layers))
