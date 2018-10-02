#!/usr/bin/env python3

# Detect simple cycles using NetworkX
# Usage: cycles.py <graph.csv >cycles.csv

import numpy as np
import networkx as nx
import sys
import argparse

G = nx.DiGraph()

while True:
	line = sys.stdin.readline()
	if not line: break
	u, v = line.strip().split(',')
	G.add_edge(u, v)

cycles = nx.simple_cycles(G)
for cycle in cycles:
	if len(cycle) > 1: # avoid self-cycles	
		print(', '.join(cycle))
