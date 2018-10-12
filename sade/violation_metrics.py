import networkx as nx
import collections


def back_call_violation_index(G, layers):
    """Back call violation index"""
    bcvi = collections.defaultdict(int)
    count = collections.defaultdict(int)
    for u, v in G.edges():
        if layers[u] < layers[v]:
            bcvi[layers[u]] += 1
        count[layers[u]] += 1

   
    for key in count:
        bcvi[key] = bcvi[key] / count[key]

    return bcvi


def skip_call_violation_index(G, layers):
    """Skip call violation index"""
    scvi = collections.defaultdict(int)
    count = collections.defaultdict(int)
    for u, v in G.edges():
        if layers[u] > 1 + layers[v]:
            scvi[layers[u]] += 1
        count[layers[u]] += 1

    for key in count:
        scvi[key] = scvi[key] / count[key]

    return scvi
