from scipy.sparse import *
import copy
import numpy as np
import sys

def kl_div(p, q):
    temp = - np.log (p / q)
    prod = temp * p;
    return np.sum(prod)

class Cluster:

    def __init__(self, features, feature_vector, num_tuples, total_tuples):
        self.features = features
        # self.features.sort()
        self.feature_vector = feature_vector
        self.num_tuples = num_tuples
        self.total_tuples = total_tuples
        self._probability = None
        self._cond_attr = None

    def calculate_distributional_cluster_features(self):
        self._probability = self.num_tuples / self.total_tuples
        self._cond_attr = np.sum(self.feature_vector, axis=0) / np.sum(self.feature_vector)
        return self._probability, self._cond_attr

    @property
    def probability(self):
        if self._probability == None:
            self.calculate_distributional_cluster_features()
        return self._probability

    @property
    def cond_attr(self):
        if self._cond_attr == None:
            self.calculate_distributional_cluster_features()
        return self._cond_attr

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
        c = Cluster(features=copy.deepcopy(a.features)+copy.deepcopy(b.features),
                    feature_vector=None,
                    num_tuples=a.num_tuples + b.num_tuples,
                    total_tuples=a.total_tuples)
        c._probability = a.probability + b.probability

        c._cond_attr = a.probability / c.probability * a.cond_attr + b.probability / c.probability * b.cond_attr

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
    memo = {}

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

                if (initial_clusters[i], initial_clusters[j]) in memo:
                    c, dI = memo[i, j]
                else:
                    c, dI = Cluster.merge_clusters(initial_clusters[i], initial_clusters[j])
                    memo[initial_clusters[i], initial_clusters[j]] = (c, dI)

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
        merged.append(c)

        initial_clusters = merged

        n -= 1

    return initial_clusters


if __name__  == '__main__':
    t1 = np.array([100, 1, 1, 1])
    t2 = np.array([0, 0, 2, 0])
    c1 = Cluster(('t1',), t1, 1, 2)
    c3 = Cluster(('t2',), t1, 1, 2)
    c2 = Cluster(('t3',), t2, 1, 2)

    l = [c1, c2, c3]

    res = agglomerative_information_bottleneck_clustering(l, 2)

    print(res)
