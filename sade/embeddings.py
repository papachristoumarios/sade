#!/usr/bin/env python3

# Source Code Document Embeddings Module

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

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO)


def get_areas():
    result = list(filter(os.path.isdir, os.listdir(os.curdir)))
    return set(result)


def source_code_document_embeddings(extensions):
    files = []
    for ext in extensions:
        files.extend(list_files('.', ext))

    data_samples = []
    for filename in files:
        print(filename)
        with open(filename) as f:
            try:
                content = f.read()
                data_samples.append(content)
            except BaseException:
                continue
    stopwords = build_stoplist(data_samples, 10)
    stopwords_regex = '|'.join(stopwords)

    for i in range(len(data_samples)):
        data_samples[i] = remove_stopwords(data_samples[i])

    print('Build dataset')
    taggeddocs = []

    for filename, sample in zip(files, data_samples):
        lines = sample.splitlines()
        words = []
        for line in lines:
            words.extend(line.split())

        td = TaggedDocument(words=words, tags=[filename])
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


def preprocess_data_samples(data_samples):
    # Remove first comment (heuristic for copyright related stuff)
    long_comment_regex = r'/\*[^\*/]*\*/'
    for i in range(len(data_samples)):
        first_comment = re.search(long_comment_regex, data_samples[i])
        if first_comment is not None:
            start, end = first_comment.span()
            data_samples[i] = data_samples[i][:end]

    # Remove stopwords
    for i in range(len(data_samples)):
        data_samples[i] = remove_stopwords(data_samples[i]).split()

    # Split camel-case and Lemmatize
    for i, sample in enumerate(data_samples):
        result = []
        for word in sample:
            components = split_underscores(word)

            for c in components:
                doc = nlp(c)
                for token in doc:
                    result.extend(token.lemma_)

        data_samples[i] = result


def build_stoplist(data_samples, most_common=100):
    words = []
    for x in data_samples:
        words.extend(x.split())
    print('Counting words')

    stopwords = []
    try:
        counter = pickle.load(open('gg_stoplist.pickle', 'rb'))
    except BaseException:
        counter = collections.Counter(words)
        pickle.dump(counter, open('gg_stoplist.pickle', 'wb'))
    finally:
        for w in counter.most_common(most_common):
            stopwords.append(w[0])
    print('Done Counting')
    return stopwords


def camel_case_split(identifier):
    matches = finditer(
        '.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)',
        identifier)
    return [m.group(0) for m in matches]


def split_underscores(s):
    return s.split('_')


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


if __name__ == '__main__':
    os.chdir(sys.argv[1])
    source_code_document_embeddings(['.c', '.h'])
