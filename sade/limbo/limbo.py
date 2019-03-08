from scipy.sparse import *
import numpy as np

def kl_div(p, q):
    temp = - np.log (p / q)
    prod = temp * p;
    return np.sum(prod)

class Cluster:

    def __init__(self, feature_vector, num_tuples, total_tuples):
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

    @staticmethod
    def merge_clusters(a, b):
        c = Cluster(feature_vector=None,
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

if __name__  == '__main__':
    t1 = np.array([100, 1, 1, 1])
    t2 = np.array([0, 0, 2, 0])
    c1 = Cluster(t1, 1, 2)
    c2 = Cluster(t2, 1, 2)
    c3, dI = Cluster.merge_clusters(c1, c2)
    print(c3, dI)
