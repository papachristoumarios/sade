import numpy as np
from sklearn.metrics import silhouette_samples
from gensim.models import Doc2Vec
import collections

def load_clusters(bunchfile, model):
    clusters = collections.defaultdict(list)

    with open(bunchfile) as f:
        lines = f.read().splitlines()

    for line in lines:
        name, files = line.split('= ')
        files = files.split(', ')
        try:
            name = int(name)
        except:
            pass
        for filename in files:
            clusters[name].append(model.docvecs[filename])

    X, y = [], []

    for key, val in clusters.items():
        for emb in val:
            X.append(emb)
            y.append(key)

    X = np.array(X)
    y = np.array(y)

    return X, y, clusters

def silhouette_score(bunch, embeddings_filename, aggregation='mean_all'):

    model = Doc2Vec.load(embeddings_filename)
    X, y, _ = load_clusters(bunch, model)

    sihlouettes = silhouette_samples(X, y, metric='cosine')

    if aggregation == 'mean_all':
        return sihlouettes.mean()
    elif aggregation == 'mean_cluster':
        unique = np.unique(y)
        results = np.zeros(len(unique), dtype=np.float64)
        for cluster_label in unique:
            results[cluster_label] = sihlouettes[np.where(y == cluster_label)].mean()
        return results
    else:
        return sihlouettes
