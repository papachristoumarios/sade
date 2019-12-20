"""
    LIMBO Clustering Algorithm implementation
    DOI: 10.1109/TSE.2005.25
    Usage: limbo.py -h
"""

from scipy.sparse import *
import argparse
import copy
import pickle
import numpy as np
import sys
import bisect
import collections
import sade.helpers
np.warnings.filterwarnings('ignore')


def kl_div(p, q):
    temp = - np.log (p / q)
    prod = temp * p;
    return np.nansum(prod)


class DCFNode:
    '''
    DCF Node object
    Args:
        B (int): The maximum number of keys each node can hold.
    '''
    def __init__(self, B):
        self.B = B
        self.keys = []
        self.values = []
        self.leaf = True
        self.merged = None
        self.dI = None

    def add(self, key, value):
        '''
        Adds a key-value pair to the node.
        '''
        if not self.keys:
            self.keys.append(key)
            self.values.append([value])
            return None

        for i, item in enumerate(self.keys):
            if key == item:
                self.values[i].append(value)
                break

            elif key < item:
                self.keys = self.keys[:i] + [key] + self.keys[i:]
                self.values = self.values[:i] + [[value]] + self.values[i:]
                break

            elif i + 1 == len(self.keys):
                self.keys.append(key)
                self.values.append([value])
                break

    def split(self):
        '''
        Splits the node into two and stores them as child nodes.
        '''
        left = DCFNode(self.B)
        right = DCFNode(self.B)
        mid = self.B // 2

        left.keys = self.keys[:mid]
        left.values = self.values[:mid]

        right.keys = self.keys[mid:]
        right.values = self.values[mid:]

        self.keys = [right.keys[0]]
        self.values = [left, right]
        self.leaf = False

    def is_full(self):
        '''
        Returns True if the node is full.
        '''
        return len(self.keys) == self.B

    def __repr__(self):
        if not self.leaf:
            return 'Keys: {} Children: {}'.format(str(self.keys), str(self.values))
        else:
            return 'Keys: {}'.format(str(self.keys))

    def merge(self):
        ''' Merges a node's keys to a cluster '''
        if len(self.keys) == 1:
            self.merged = self.keys[0]
            self.dI = 0
        elif len(self.keys) >= 2:
            temp_c, temp_dI = Cluster.merge_clusters(self.keys[0], self.keys[1])
            for i in range(2, len(self.keys)):
                temp_c, temp_dI = Cluster.merge_clusters(temp_c, self.keys[i])
            self.merged = temp_c
            self.dI = temp_dI
        return self.merged



class DCFTree:
    '''
    DCF Tree
    Implementation of B+ Tree: https://gist.github.com/savarin/69acd246302567395f65ad6b97ee503d
    Args:
        B (int): The maximum number of keys each node can hold.
    '''
    def __init__(self, B=3, S=sys.maxsize, E=sys.maxsize):
        self.root = DCFNode(B)
        # XXX Implement space bound
        self.max_number_of_nodes = S // (E * B)
        self.number_of_nodes = 0

    def _find(self, node, key):
        '''
        For a given node and key, returns the index where the key should be
        inserted and the list of values at that index.
        The index corresponds to the minimum information loss
        '''
        minimum_dI = sys.maxsize
        argmin = -1

        for i, item in enumerate(node.keys):
            _, dI = Cluster.merge_clusters(key, item)
            if dI <= minimum_dI:
                minimum_dI = dI
                argmin = i


        return node.values[i], i

    def _merge(self, parent, child, index):
        '''
        For a parent and child node, extract a pivot from the child to be
        inserted into the keys of the parent. Insert the values from the child
        into the values of the parent.
        '''
        parent.values.pop(index)
        pivot = child.keys[0]

        for i, item in enumerate(parent.keys):
            if pivot < item:
                parent.keys = parent.keys[:i] + [pivot] + parent.keys[i:]
                parent.values = parent.values[:i] + child.values + parent.values[i:]
                break

            elif i + 1 == len(parent.keys):
                parent.keys += [pivot]
                parent.values += child.values
                break

    def insert(self, key, value):
        '''
        Inserts a key-value pair after traversing to a leaf node. If the leaf
        node is full, split the leaf node into two.
        '''
        parent = None
        child = self.root

        while not child.leaf:
            parent = child
            child, index = self._find(child, key)

        child.add(key, value)

        if child.is_full():
            child.split()

            if parent and not parent.is_full():
                self._merge(parent, child, index)

        self.number_of_nodes += 1


    def retrieve(self, key):
        '''
        Returns a value for a given key, and None if the key does not exist.
        '''
        child = self.root

        while not child.leaf:
            child, index = self._find(child, key)

        for i, item in enumerate(child.keys):
            if key == item:
                return child.values[i]

        return None

    def __repr__(self):
        return self.root.__repr__()

    def cluster_leaves(self):
        ''' Cluster the leaves of the tree for use with AIB '''
        q = collections.deque([self.root])
        self.leaves = []

        while q:
            current = q.popleft()
            if current.leaf:
                self.leaves.append(current)
            else:
                for child in current.values:
                    q.append(child)

        clusters = []
        for leaf in self.leaves:
            leaf.merge()
            if leaf.dI != None:
                clusters.append(leaf.merged)

        return clusters


class Cluster:

    def __init__(self, features, feature_vector, num_tuples, total_tuples):
        self.features = features
        self.feature_vector = feature_vector
        self.num_tuples = num_tuples
        self.total_tuples = total_tuples
        if self.num_tuples == 1:
            self.calculate_distributional_cluster_features()

    def calculate_distributional_cluster_features(self):
        self.probability = self.num_tuples / self.total_tuples
        self.cond_attr = self.feature_vector.astype(np.float64) / np.sum(self.feature_vector)
        return self.probability, self.cond_attr

    def __lt__(self, other):
        _, dI = Cluster.merge_clusters(self, other)
        return dI < 0

    def __repr__(self):
        return str(self.features)

    def __eq__(self, other):
        return self.features == other.features

    def __hash__(self):
        return hash(self.features)

    @staticmethod
    def merge_clusters(a, b):
        c = Cluster(features=a.features+b.features,
                    feature_vector=None,
                    num_tuples=a.num_tuples + b.num_tuples,
                    total_tuples=a.total_tuples)


        c.probability = a.probability + b.probability

        c.cond_attr = a.probability / c.probability * a.cond_attr + b.probability / c.probability * b.cond_attr

        # Calculate dI
        D_KL_a = kl_div(a.cond_attr, c.cond_attr)
        D_KL_b = kl_div(b.cond_attr, c.cond_attr)

        D_JS = a.probability / c.probability * D_KL_a + b.probability / c.probability * D_KL_b
        dI = D_JS * (a.probability + b.probability)

        return c, dI


def agglomerative_information_bottleneck_clustering(initial_clusters, n_clusters):
    """Agglomerative Information Bottleneck (AIB) algorithm.
        Args:
            initial_clusters: A list of lists containing the initial clusters (Produced by the DCFTree leaves)
            n_clusters: Desired Number of Clusters
    """

    n = len(initial_clusters)

    if n < n_clusters:
        raise Exception('Please decrease B')

    while n > n_clusters:
        # Minimum indexes
        argmin_i = 0
        argmin_j = 0

        # Minimum information loss
        minimum_dI = sys.maxsize

        # New cluster to replace existing
        argmin = None

        for i in range(n):
            for j in range(n):
                if i == j:
                    continue

                c, dI = Cluster.merge_clusters(initial_clusters[i], initial_clusters[j])
                if dI <= minimum_dI:
                    minimum_dI = dI
                    argmin = c
                    argmin_i = i
                    argmin_j = j

        # Merge two lists
        merged = []
        for i in range(n):
            if i not in [argmin_i, argmin_j]:
                merged.append(initial_clusters[i])

        # Append merged cluster
        merged.append(argmin)

        initial_clusters = merged


        n -= 1

    result = {}

    for i, cluster in enumerate(initial_clusters):
        result[i] = list(cluster.features)

    return result


def limbo(initial_clusters, n_clusters, B, S):
    """
        The LIMBO Clustering Algorithm
        Args:
            initial_clusters: An array of Cluster objects
            n_clusters: Number of desired clusters
            B: Branching Factor of the DCFTree
            S: Spatial Factor of the DCFTree
    """

    # Phase 1: Insert to DCF Tree
    dcf_tree = DCFTree(B, S)

    for cluster in initial_clusters:
        dcf_tree.insert(cluster, cluster)

    # Phase 2: Apply AIB Algorithm to the tree leaves
    # Collect merged leaves
    aib_initial_clusterings = dcf_tree.cluster_leaves()

    # TODO Add phase 3 / naming

    return agglomerative_information_bottleneck_clustering(aib_initial_clusterings, n_clusters=n_clusters)


def preprocess_bow(bow_filename):

    bow = pickle.load(open(bow_filename, 'rb'))
    bow_filtered = [(key, np.array(val[0])) for key, val in bow.items() if sum(val[0]) != 0]
    total_tuples = len(bow_filtered)
    initial_clusters = []

    for cluster_label, feature_vector in bow_filtered:
        c = Cluster((cluster_label, ), feature_vector=feature_vector, num_tuples=1, total_tuples=total_tuples)
        initial_clusters.append(c)

    return initial_clusters


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(usage='LIMBO Clustering Algorithm')

    argparser.add_argument('-i', help='BoW File')
    argparser.add_argument('-n', help='Number of clusters', type=int)
    argparser.add_argument('--aib', help='Naively run Agglomerative Information Bottleneck', action='store_true')
    argparser.add_argument('-B', help='DCF-tree branching factor', type=int, default=3)
    argparser.add_argument('-S', help='DCF-tree space factor', type=int, default=sys.maxsize)
    argparser.add_argument('--export', help='Export type', default='bunch')

    args = argparser.parse_args()

    initial_clusters = preprocess_bow(args.i)

    if args.aib:
        result = agglomerative_information_bottleneck_clustering(initial_clusters=initial_clusters, n_clusters=args.n)
    else:
        while True:
            try:
                result = limbo(initial_clusters=initial_clusters, n_clusters=args.n, B=args.B, S=args.S)
                break
            except:
                args.B = args.B // 2
                
    if args.export == 'bunch':
        print(sade.helpers.generate_bunch(result))
    elif args.export == 'json':
        print(json.dumps(result))
