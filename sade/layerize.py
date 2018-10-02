#!/usr/bin/env python3

# Detect simple cycles using NetworkX
# Usage: cycles.py <graph.csv >cycles.csv

import numpy as np
import networkx as nx
import sys

def calculate_score(succ):
    return 0

G = nx.DiGraph()

while True:
	line = sys.stdin.readline()
	if not line: break
	u, v = line.strip().split(',')
	G.add_edge(u, v)

opt = - (sys.maxsize - 1)

for s in G.nodes:
    succ = nx.bfs_sucessors(G, s)
    score = calculate_score(succ)
    opt = max(opt, score)
