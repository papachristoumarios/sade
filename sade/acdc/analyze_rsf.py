import sys
import collections
import numpy as np

lines = [s.split()[1:] for s in sys.stdin.read().splitlines()]

clusters = collections.defaultdict(list) 

for line in lines: 
    clusters[line[0]].append(line[1])

sizes = np.zeros(len(clusters))

for i, cluster in enumerate(clusters):
    sizes[i] = len(clusters[cluster])

print('Number of clusters: ', len(clusters))
print('Largest cluster size: ', np.max(sizes))
print('Smallest cluster size: ', np.min(sizes))
print('Average cluster size: ', np.mean(sizes))
print('Standard Deviation: ', np.std(sizes))
print('Median cluster: ', np.median(sizes))

