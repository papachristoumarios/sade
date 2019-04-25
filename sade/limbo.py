from scipy.sparse import *
import argparse
import copy
import pickle
import numpy as np
import sys
import bisect

def kl_div(p, q):
    temp = - np.log (p / q)
    prod = temp * p;
    return np.nansum(prod)



class BTreeNode:

    def __init__(self, B, leaf):
        # Degree and leaf property
        self.B = B
        self.leaf = leaf

        # Keys and children
        self.keys = (2*B - 1)*[None]
        self.children = (2*B) * [None]

        # Number of keys
        self.n = 0

    def __repr__(self):
        return 'Keys: {} Children: {}'.format(str(self.keys), str(self.children))

    def search(self, key):
        i = 0

        while i < self.n and key > keys[i]:
            i += 1

        if keys[i] == key:
            return self

        if self.leaf:
            return None

        return self.children[i].search(key)

    def insert_non_full(self, key):

        i = self.n - 1

        if self.leaf:
            # Insert the key

            while i >= 0 and self.keys[i] > key:
                self.keys[i + 1] = self.keys[i]
                i -= 1

            self.keys[i+1] = key;

            self.n += 1

        else:

            while i >= 0 and self.keys[i] > key:
                i -= 1

            if self.children[i + 1].n == 2 * self.B - 1:
                self.split_child(i + 1, self.children[i + 1])

                if self.keys[i + 1] < key:
                    i += 1

            self.children[i + 1].insert_non_full(key)

    def split_child(self, i, y):

        # Shallow copy
        z = copy.copy(y)
        z.n = self.B - 1

        for j in range(self.B - 1):
            z.keys[j] = y.keys[j + self.B]

        if not y.leaf:
            for j in range(self.B - 1):
                z.children[j] = y.children[j + self.B]
        y.n = self.B - 1

        for j in range(self.n, i, -1):
            self.children[j + 1] = self.children[j]

        self.children[i + 1] = z

        for j in range(self.n - 1, i - 1, -1):
            self.keys[j+1] = self.keys[j]

        self.keys[i] = y.keys[self.B-1];

        self.n += 1

    def collect_leaves(self, result):
        if self.leaf and self.n > 0:
            result.append(self)
            return result
        else:
            for i in range(self.n):
                self.children[i].collect_leaves(result)

class BTree:

    def __init__(self, B):
        self.B = B
        self.root = None

    def traverse(self):
        if self.root != None:
            self.root.traverse()

    def search(self, key):
        if self.root != None:
            self.root.search(key)

    def __repr__(self):
        return self.root.__repr__()

    def insert(self, key):

        # Root is created
        if self.root == None:
            self.root = BTreeNode(self.B, True)
            self.root.keys[0] = key
            self.root.n = 1

        else:
            # The B-Tree is full so we need to change the root by splitting
            if self.root.n == 2 * self.B - 1:
                s = BTreeNode(self.B, False)
                s.children[0] = self.root

                # Split and insert
                s.split_child(0, self.root)

                i = 0
                if s.keys[0] < key:
                    i += 1

                s.children[i].insert_non_full(key)

                # Change root
                self.root = s

            else:

                self.root.insert_non_full(key)

class DCFNode(BTreeNode):

    def __init__(self, B, leaf):
        super(DCFNode, self).__init__(B, leaf)
        self._merged = None
        self._dI = None

    @property
    def merged(self):
        if self.n == 1:
            self._dI = 0
            self.merged = self.keys[0]
        elif self.n > 1:
            temp_c, temp_dI = sade.limbo.Cluster.merge_clusters(self.keys[0], self.keys[1])
            for i in range(2, self.n):
                temp_c, temp_dI = sade.limbo.Cluster.merge_clusters(temp_c, self.keys[i])
            self._merged = temp_c
            self._dI = temp_dI

    def insert_non_full(self, key):

        i = self.n - 1

        argmin = 0
        minimum_dI = sys.maxsize

        for j in range(self.n):
            _, temp_dI = sade.limbo.Cluster.merge_clusters(self.keys[j], key)
            if temp_dI < minimum_dI:
                minimum_dI = temp_dI
                argmin = j

        if self.leaf:
            # Insert the key

            while i >= argmin:
                self.keys[i + 1] = self.keys[i]
                i -= 1

            self.keys[i+1] = key;

            self.n += 1

        else:

            while i >= argmin: i -= 1

            if self.children[i + 1].n == 2 * self.B - 1:
                self.split_child(i + 1, self.children[i + 1])

                if self.keys[i + 1] < key:
                    i += 1

            self.children[i + 1].insert_non_full(key)

class DCFTree(BTree):

    def __init__(self, B, S):
        super(DCFTree, self).__init__(B)
        self.S = S
        self.leaves = None

    @property
    def border(self):
        if self.leaves == None:
            self.leaves = self.root.collect_leaves([])
        return self.leaves

    def cluster_leaves(self):
        self.cluster_leaves = [b.merged for b in self.border]
        return self.cluster_leaves


class Cluster:

    def __init__(self, features, feature_vector, num_tuples, total_tuples):
        self.features = features
        # self.features.sort()
        self.feature_vector = feature_vector
        self.num_tuples = num_tuples
        self.total_tuples = total_tuples
        if self.num_tuples == 1:
            self.calculate_distributional_cluster_features()

    def calculate_distributional_cluster_features(self):
        self.probability = self.num_tuples / self.total_tuples
        # self._cond_attr = np.sum(self.feature_vector, axis=0) / np.sum(self.feature_vector)
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

    return initial_clusters


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
        dcf_tree.insert(c)

    # Phase 2: Apply AIB Algorithm to the tree leaves
    # Collect merged leaves
    # XXX Collect the parent of leaves
    aib_initial_clusterings = dcf_tree.cluster_leaves()

    # TODO Add phase 3 / naming

    return agglomerative_information_bottleneck_clustering(aib_initial_clusterings, n_clusters=n_clusters)


def preprocess_bow(bow_filename):

    bow = pickle.load(open(bow_filename, 'rb'))
    bow_filtered = [(key, np.array(val)) for key, val in bow.items() if sum(val) != 0]
    total_tuples = len(bow_filtered)
    initial_clusters = []

    for cluster_label, feature_vector in bow_filtered:
        c = Cluster((cluster_label, ), feature_vector=feature_vector, num_tuples=1, total_tuples=total_tuples)
        initial_clusters.append(c)

    return initial_clusters


# if __name__  == '__main__':
#     t1 = np.array([100, 1, 1, 1])
#     t2 = np.array([0, 0, 2, 0])
#     c1 = Cluster(('t1',), t1, 1, 2)
#     c3 = Cluster(('t2',), t1, 1, 2)
#     c2 = Cluster(('t3',), t2, 1, 2)
#
#     l = [c1, c2, c3]
#
#     res = agglomerative_information_bottleneck_clustering(l, 2)
#
#     print(res)
#
# t = DCFTree(3, 2)
# N = 100
# for i in range(N):
#     tt = np.random.randint(100, size=4)
#     c = Cluster(('t' + str(i),), tt, 1, N)
#     t.insert(c)
#
# print(t.border)

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(usage='LIMBO Clustering Algorithm')

    argparser.add_argument('-i', help='BoW File')
    argparser.add_argument('-n', help='Number of clusters', type=int)
    argparser.add_argument('--aib', help='Naively run Agglomerative Information Bottleneck', action='store_true')
    argparser.add_argument('-B', help='DCF-tree branching factor')
    argparser.add_argument('-S', help='DCF-tree space factor')

    args = argparser.parse_args()

    initial_clusters = preprocess_bow(args.i)

    print(initial_clusters)

    if args.aib:
        print(agglomerative_information_bottleneck_clustering(initial_clusters=initial_clusters, n_clusters=args.n))
