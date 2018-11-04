import subprocess
import os
import sys

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
def generate_bunch(partition, outfile):
	with open(outfile, 'w+') as f:
		for key, val in partition.items():
			f.write('{} = {}\n'.format(str(key), ', '.join(map(str, val))))
