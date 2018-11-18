# Simple community detection cli tool
# Supports directed graphs using bipartite network transformation
# Usage: simple_community_detection.py -h
# Author: Marios Papachristou

import community
import networkx as nx
import sys
import collections
import pprint
import numpy as np
import argparse
import sade.helpers
import json


def get_communities(partition):
    communities = collections.defaultdict(list)

    for key, val in partition.items():
        communities[val].append(key)

    return communities


def community_statistics(communities):
    counts = []
    for key, val in communities.items():
        counts.append(len(val))
    counts = np.array(counts)

    print('Total nodes: ', np.sum(counts))
    print('Number of communities', len(communities))
    print('Mean Community Size:', np.mean(counts))
    print('Standard Deviation (non-biased): ', np.std(counts))


def best_partition_bipartite(G):
    def _union(u, v):
        w = parent[u]
        while parent[w] != w:
            w = parent[w]
        parent[v] = w

    # H is a bipartite network
    H = nx.Graph()
    mapping = {}
    inv_mapping = {}

    # Bipartite transformation
    for u in G.nodes():
        hu = hash(u)
        H.add_node(u)
        H.add_node(hu)
        mapping[u] = hu
        inv_mapping[hu] = u

    for u, v in G.edges():
        H.add_edge(u, hash(v))

    partition = community.best_partition(H)

    # cluster to communities
    communities = collections.defaultdict(set)

    parent = {}

    for val in partition.values():
        parent[val] = val

    # Union-find to join communities with common x and hash(x)
    for u in G.nodes():
        if partition[u] != partition[mapping[u]]:
            _union(partition[u], partition[mapping[u]])

    for key, val in partition.items():
        if not isinstance(key, int):
            communities[parent[val]] |= {key}
        else:
            communities[parent[val]] |= {inv_mapping[key]}

    for key, val in communities.items():
        communities[key] = list(val)

    return communities


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        description='Simple Community detection script')
    argparser.add_argument(
        '--bunchify',
        help='Generate bunch file (default is json)',
        action='store_true')
    argparser.add_argument(
        '--stats',
        help='Print statistics to stdout',
        action='store_true')
    argparser.add_argument(
        '--directed',
        help='Run directed analogue with transformation to bipartite network',
        action='store_true')
    argparser.add_argument(
        '-c',
        help='Contract Call Graph Using a Module/Layer Definition file',
        default='')
    args = argparser.parse_args()

    edges = sys.stdin.read().splitlines()

    if args.directed:
        G = nx.DiGraph()
    else:
        G = nx.Graph()

    for edge in edges:
        parts = edge.split()
        if len(parts) == 2:
            u, v = parts
            G.add_edge(*parts)
        elif len(parts) == 3:
            u, v, w = parts
            G.add_edge(u, v, weight=float(w))

    if args.c != '':
        contraction = json.loads(open(args.c, 'r').read())
        G = sade.helpers.contract_graph(G, contraction)

    if args.directed:
        communities = best_partition_bipartite(G)
    else:
        partition = community.best_partition(G)
        communities = get_communities(partition)

    if args.bunchify:
        print(sade.helpers.generate_bunch(communities))
    else:
        print(json.dumps(communities, indent=4, separators=(',', ': ')))

    if args.stats:
        community_statistics(communities)
