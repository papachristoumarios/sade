#!/usr/bin/env python3

# Area Commits Module

import os
import spacy
nlp = spacy.load('en_core_web_sm')
import re
import pickle
import string
import glob
import sys
import collections
import subprocess
import gensim
from gensim.models.doc2vec import TaggedDocument
from gensim.parsing.preprocessing import preprocess_string, remove_stopwords
import logging
from matplotlib import pyplot as plt
import numpy as np
from helpers import cmd
from git_commits import *

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO)


def train_model_from_commits(areas):
    # Train doc2vec model from unique area commits
    assert(len(areas) > 0)

    print('Get unique')
    unique_commits = get_unique_commits(areas)
    for a in areas:
        print(len(unique_commits[a]))

    print('Build dataset')
    taggeddocs = []

    for area in areas:
        for _hash in unique_commits[area]:
            try:
                lines = commit_message(_hash)
            except BaseException:
                continue
            words = []
            for line in lines:
                words.extend(line.split())

            td = TaggedDocument(words=words, tags=[area])
            taggeddocs.append(td)

    print('Generated dataset')

    model = gensim.models.Doc2Vec(
        window=8,
        dm=0,
        hs=0,
        min_count=2,
        alpha=0.1,
        vector_size=200,
        min_alpha=0.0001,
        epochs=50,
        workers=6,
        sample=1e-5,
        dbow_words=1,
        negative=5)
    model.build_vocab(taggeddocs)
    model.train(
        taggeddocs,
        total_examples=model.corpus_count,
        epochs=model.iter)
    model.save('embeddings.bin')

    return model


def split_commit_message(_hash, model, areas):
    # Split a commit message using a Doc2Vec model
    result = collections.defaultdict(list)
    lines = commit_message(_hash)

    for line in lines:
        line = line.split('. ')
        for sentence in line:
            v = model.infer_vector(sentence)
            similar = model.docvecs.most_similar([v], topn=len(areas))

            for key, val in similar:
                if key in areas:
                    result[key].append(sentence)
                    break

    for key, val in result.items():
        result[key] = '. '.join(val)

    return result


def fix_commits(_hash, processed_commit_messages):
    # Fix and redo the commits
    files = changed_files(_hash)
    result = collections.defaultdict(list)
    current_branch = cmd('basename $(git symbolic-ref HEAD)')[0]

    for area in processed_commit_messages:
        for f in files:
            if f.startswith(area):
                result[area].append(f)

    # Reset
    os.system('git checkout -b {}-layering'.format(_hash))
    os.system('git reset --hard {}^1'.format(_hash))

    # Split the commit
    for area, files in result.items():
        for f in files:
            os.system('git checkout {} {}'.format(_hash, f))
            os.system('git add -u')
            os.system(
                'git commit -m "{}"'.format(processed_commit_messages[area]))

    # Do a merge
    os.system('git merge {}'.format(current_branch))


def visualize(title, curr_hash, violations):
    def bar_plot(keys, vals, title, curr_hash):
        index = np.arange(len(keys))
        plt.bar(index, vals)
        plt.xlabel('Areas')
        plt.ylabel('Number of Layering Violations')
        plt.xticks(index, keys, rotation=30)
        plt.title('Layering Violations of ' + title + ' until ' + curr_hash)
        plt.show()

    vals = [len(x) for x in violations.values()]
    keys = list(violations.keys())
    bar_plot(keys, vals, title, curr_hash)

def plot_area_violations(source, others):
    violations = {}
    for x in others:
        violations[x] = areas_violations(x, source)

    curr_hash  = last_hash()

    visualize(source, curr_hash, violations)


def get_areas():
    result = list(filter(os.path.isdir, os.listdir(os.curdir)))
    return set(result)


def build_stoplist(data_samples, most_common=100):
    words = []
    for x in data_samples:
        words.extend(x.split())
    print('Counting words')

    stopwords = []
    try:
        counter = pickle.load(open('stoplist.pickle', 'rb'))
    except BaseException:
        counter = collections.Counter(words)
        pickle.dump(counter, open('stoplist.pickle', 'wb'))
    finally:
        for w in counter.most_common(most_common):
            stopwords.append(w[0])
    print('Done Counting')
    return stopwords

if __name__ == '__main__':
    os.chdir(sys.argv[1])
    # plot_area_violations('kernel', ['drivers', 'arch', 'fs', 'crypto', 'scripts', 'security', 'firmware', 'ipc', 'sound'])
