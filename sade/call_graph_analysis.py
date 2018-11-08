#!/usr/bin/env python3

import networkx as nx
import argparse
import sys
import pickle

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Call graph analysis tool')
    argparser.add_argument('--delimiter', help='Delimiter to print table', default=':')
    argparser.add_argument('--eol', help='End of line', default='')
    args = argparser.parse_args()

    edges = sys.stdin.read().splitlines()
    G = nx.DiGraph()
    for edge in edges:
        G.add_edge(*edge.split())


    stats = [
        ('Number of Nodes', len(G)),
        ('Number of Edges', G.number_of_edges()),
        ('Strongly Connected Components', int(nx.number_strongly_connected_components(G))),
        ('Average Clustering Coefficient', nx.average_clustering(G))]

    print('Statistics', args.delimiter, ' ', args.eol)    
    for key, val in stats:
        print('{} {} {} {}'.format(key, args.delimiter, val, args.eol))
