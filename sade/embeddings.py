#!/usr/bin/env python3

# Source Code Document Embeddings Module

import os
import spacy
nlp = spacy.load('en_core_web_sm')
import re
import pickle
import argparse
import json
import string
import glob
import sys
import collections
import subprocess
import gensim
from gensim.models.doc2vec import TaggedDocument
from gensim.parsing.preprocessing import preprocess_string, remove_stopwords
import logging
import numpy as np
import sade.helpers

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO)


def get_areas():
    result = list(filter(os.path.isdir, os.listdir(os.curdir)))
    return set(result)


def source_code_document_embeddings(extensions, modules=None, outfile='embeddings.bin'):
    if modules != None:
        modules = json.loads(open(modules, 'r').read())


    files = []
    for ext in extensions:
        files.extend(sade.helpers.list_files('.', ext))

    data_samples = []
    for filename in files:
        print(filename)
        with open(filename) as f:
            try:
                content = f.read()
                data_samples.append(content)
            except BaseException:
                continue
    stopwords = build_stoplist(data_samples)

    data_samples = preprocess_data_samples(data_samples=data_samples, stopwords=stopwords)


    print('Build dataset')
    taggeddocs = []

    for filename, sample in zip(files, data_samples):

        if modules == None:
            td = TaggedDocument(words=sample, tags=[sade.helpers.basename(filename)])
        else:
            td = TaggedDocument(words=sample, tags=[module[filename]])

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
    model.save(outfile)

    return model


def preprocess_data_samples(data_samples, stopwords):

    # Remove first comment (heuristic for copyright related stuff)
    long_comment_regex = r'/\*[^\*/]*\*/'
    for i in range(len(data_samples)):
        first_comment = re.search(long_comment_regex, data_samples[i])
        if first_comment is not None:
            start, end = first_comment.span()
            data_samples[i] = data_samples[i][:end]

    stopwords_regex = '|'.join(map(re.escape, stopwords))

    for i in range(len(data_samples)):
        data_samples[i] = re.sub(stopwords_regex, '', data_samples[i])

    # Split camel-case and Lemmatize
    for j, sample in enumerate(data_samples):
        result = []
        words = re.split('\s+', sample)
        for i, word in enumerate(words):
            components = pipelined_removals(word)
            words[i] = ' '.join(components)
        words = ' '.join(words)


        doc = nlp(words)
        for token in doc:
            result.append(token.lemma_.lower())

        data_samples[j] = result

    return data_samples


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
    matches = re.finditer(
        '.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)',
        identifier)
    return [m.group(0).lower() for m in matches]


def split_underscores(s):
    return s.split('_')

def remove_nonalpha(s):
    return ''.join([x for x in s if x.isalpha()])

def expand(s):
    expanders = ['(', ')', '{', '}', '[', ']', '%', '\n']
    return list(filter(lambda x : x != '', multi_split(expanders, s)))

def multi_split(delimiters, string, maxsplit=0):
    regexPattern = '|'.join(map(re.escape, delimiters))
    return re.split(regexPattern, string, maxsplit)

def pipelined_removals(s, pipeline=[expand, split_underscores, camel_case_split], cleaner=remove_nonalpha):
    result = pipeline[0](s)
    for component in pipeline[1:]:
        temp = []
        for token in result:
            temp.extend(component(token))
        result = temp


    for i, r in enumerate(result):
        result[i] = cleaner(r)

    return result





if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Generate document embeddings')
    argparser.add_argument('-d', type=str, default='.', help='Directory')
    argparser.add_argument('-m', type=str, help='Modules')
    argparser.add_argument('-o', type=str, help='Output File', default='embeddings.bin')

    args = argparser.parse_args()

    os.chdir(args.d)

    source_code_document_embeddings(['.c', '.h'], modules=args.m, outfile=args.o)
