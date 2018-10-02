#!/usr/bin/env python3

# Covariance Calculation from doc2vec model

import numpy as np
import gensim.models
import gensim
import sys


def compute_covariance_matrix(model_name):
    model = gensim.models.Doc2Vec.load(model_name)

    doctags = list(model.docvecs.doctags)
    N = len(doctags)

    X = []

    for x in doctags:
        X.append(model.docvecs[x])

    X = np.array(X)

    # R[i, j] = R[j, i] = dot(vi, vj) / (norm(vi) * norm(vj))
    R = np.corrcoef(X)

    return doctags, R


if __name__ == '__main__':
    model_name = sys.argv[1]
    doctags, R = compute_covariance_matrix(model_name)
    np.savetxt('corrcoef.csv', R, delimiter=',')
    with open('doctags.csv', 'w+') as f:
        f.write(','.join(doctags))
