#!/usr/bin/env python3

# Covariance Calculation from doc2vec model

import numpy as np
import gensim.models
import gensim
import sys
import pickle
from helpers import get_name

def compute_covariance_matrix(model_name, to_json=True):
    model = gensim.models.Doc2Vec.load(model_name)

    doctags = list(model.docvecs.doctags)
    N = len(doctags)

    X = []

    for x in doctags:
        X.append(model.docvecs[x])

    X = np.array(X)

    # R[i, j] = R[j, i] = dot(vi, vj) / (norm(vi) * norm(vj))
    R = np.corrcoef(X)

    if to_json:
        RR = {}
        for x, dx in enumerate(doctags):
            for y, dy in enumerate(doctags):
                RR[get_name(dx), get_name(dy)] = R[x,y]
        return doctags, RR
    else:
        return doctags, R


if __name__ == '__main__':
    model_name = sys.argv[1]
    doctags, R = compute_covariance_matrix(model_name)

    pickle.dump(R, open('corrcoef.pickle', 'wb+'))
