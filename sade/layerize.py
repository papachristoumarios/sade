import numpy as np
import networkx as nx
import sys
import argparse
import collections
import pickle
import multiprocessing
from helpers import get_name


def calculate_scores(level, R):
	def _calculacte_scores_level(l):
		total, count = 0, 0
		for i in range(len(l)):
			for j in range(i + 1):
				try:
					total += R[l[i], l[j]]
					count += 1
				except:
					pass

		return total / count

	scores = {}
	for idl, l in level.items():
		scores[idl] = _calculacte_scores_level(l)

	average = np.mean([x for x in scores.values()])

	return scores, average

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


G = nx.DiGraph()
R = pickle.load(open('corrcoef.pickle', 'rb'))


while True:
		line = sys.stdin.readline()
		if not line: break
		u, v = line.strip().split(',')
		G.add_edge(get_name(u), get_name(v))

final_scores = []

for s in G.nodes():
	depth, level = bfs(G, s)
	score, avg = calculate_scores(level, R)
	print(level, avg)
