import subprocess
import os
import sys
import networkx as nx
import gensim
import numpy as np

def cmd(_cmd):
    # Get output of command
    l = subprocess.check_output(_cmd, shell=True)
    l = [x.decode('utf-8') for x in l.splitlines()]
    l = list(filter(lambda z: z.rstrip() != '', l))
    return l

def basename(x, depth=1): return x.split('/')[-depth]

def list_files(input_dir, suffix, recursive=True):
    if recursive:
        result = []
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                if file.endswith(suffix):
                    result.append(os.path.join(root, file))
    else:
        result = glob.glob('*{}'.format(suffix))
    return result

# Load data from doc2vec model
def load_data(embeddings_filename='embeddings.bin'):
    model = gensim.models.Doc2Vec.load(embeddings_filename)
    y = list(model.docvecs.doctags)
    X = []
    for x in y:
        X.append(model.docvecs[x])
    X = np.array(X)

    return X, y, model

# Generate .bunch files
def generate_bunch(partition, outfile=None):
    result = ''
    for key, val in partition.items():
        result = result + '{} = {}\n'.format(str(key), ', '.join(map(str, val)))

    if outfile == None:
        print(result)
    else:
        with open(outfile, 'w+') as f:
            f.write(result)

    return result

def contract_graph(G, contraction_mapping):
    if isinstance(G, nx.Graph):
        H = nx.Graph()
    elif isinstance(G, nx.DiGraph):
        H = nx.DiGraph()

    for (u, v) in G.edges():
        try:
            H.add_edge(contraction_mapping[u], contraction_mapping[v], weight=1)
        except:
            pass

    return H
