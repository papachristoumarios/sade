import argparse
import sade.helpers
import sys
import re
import collections
import numpy as np

argparser = argparse.ArgumentParser()
argparser.add_argument('-o')
argparser.add_argument('-i', help='Input type (rsf, bunch)', default='rsf')


args = argparser.parse_args()
clusters = collections.defaultdict(list)


if args.i == 'rsf':
    lines = [s.split()[1:] for s in sys.stdin.read().splitlines()]
    for line in lines: 
        clusters[line[0]].append(line[1])

elif args.i == 'bunch':
    lines = [s.split('=') for s in sys.stdin.read().splillines()]
    for line in lines: 
        clusters[line[0]] = line[1].split(',')
else:
    raise NotImplementedError('Filetype not supported') 

sizes = np.zeros(len(clusters))

for i, cluster in enumerate(clusters):
    sizes[i] = len(clusters[cluster])

print('Number of clusters: ', len(clusters))
print('Largest cluster size: ', np.max(sizes))
print('Smallest cluster size: ', np.min(sizes))
print('Average cluster size: ', np.mean(sizes))
print('Standard Deviation: ', np.std(sizes))
print('Median cluster: ', np.median(sizes))

if args.o != None:
    sade.helpers.generate_bunch(clusters, args.o)
