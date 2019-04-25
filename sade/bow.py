'''
    Source code Bag of Words Module
    Author: Marios Papachristou
    Usage: bow.py -h
'''



from sklearn.feature_extraction.text import CountVectorizer
import pickle
import wordninja
import functools
import os
import re
import pickle
import argparse
import json
import string
import glob
import sys
import collections
import multiprocessing
import subprocess
import gensim
from gensim.models.doc2vec import TaggedDocument
from gensim.parsing.preprocessing import preprocess_string, remove_stopwords
import logging
import numpy as np
import sade.helpers
from spacy.lang.en.lemmatizer import LOOKUP
from spacy.lang.en import English
import spacy
import sade.helpers
nlp = spacy.load('en_core_web_sm')

class BowModel(dict):

    def __init__(self, dim):
        self.dim = dim

    def __missing__(self, key):
        return np.zeros(shape=(1, self.dim), dtype=int)

    def dumpify(self):
        dumpified = {}
        for key, val in self.items():
            dumpified[key] = list(val)
        return dumpified

    @staticmethod
    def dedumpify(pickle_file):
        temp = pickle.load(open(pickle_file, 'rb'))
        bow = BowModel(len(list(temp.keys())[0]))
        for key, val in temp.items():
            bow[key] = np.array(val)

        return bow

# Ignore very small words due to tokenization errors
MIN_SIZE = 2


logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO)

def lookup(x):
    '''
        Lemmatizer lookup
    '''
    return LOOKUP.get(x, x)


def get_areas():
    result = list(filter(os.path.isdir, os.listdir(os.curdir)))
    return set(result)


def source_code_document_embeddings(
        extensions,
        modules=None,
        outfile='embeddings.bin'):
    '''
        Produce document embeddings model with gensims
        Arguments:
            extensions: file extensions to take into account
            params : model parameters
            module : module file definitions
            outfile : output binary file
    '''
    if modules is not None:
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

    data_samples = preprocess_data_samples(
        data_samples=data_samples, stopwords=stopwords)

    print('Build dataset')


    vectorizer = CountVectorizer(
        analyzer='word',
        tokenizer=lambda x: x,
        preprocessor=lambda x: x,
        token_pattern=None)

    print('Fitting BoW model')

    counts = vectorizer.fit_transform(data_samples).toarray()

    bow = BowModel(counts.shape[1])

    print('Merging')

    for i, (filename, sample) in enumerate(zip(files, data_samples)):
        base = sade.helpers.basename(filename)
        if modules is None:
            bow[base] = counts[i]
        else:
            bow[modules[base]] = bow[modules[base]] + counts[i]

    with open(outfile, 'wb+') as f:
        pickle.dump(bow.dumpify(), f)

    return bow

def _process(document):
    '''
        Document preprocessing function
        1. Remove first comment
        2. Tokenize and apply transforms to tokens
        Transformations include
        a. identifier segmentation (with unigram)
        b. cleaning forms (camel case, underscore splits)
        c. lemmatization with spaCy
    '''

    sample, stopwords_regex = document

    # Remove first comment (heuristic for copyright related stuff)
    long_comment_regex = r'/\*[^\*/]*\*/'
    first_comment = re.search(long_comment_regex, sample)
    if first_comment is not None:
        start, end = first_comment.span()
        sample = sample[:end]

    sample = re.sub(stopwords_regex, '', sample)

    # Split camel-case and Lemmatize

    result = []
    tokens = filter(lambda x: x != '', sample.split())
    components = []

    for token in tokens:
        components.extend(pipelined_removals(token))

    for word in components:
        lemma = lookup(word.lower())
        result.append(lemma)

    return list(filter(lambda x: x != '' and len(x) > MIN_SIZE, result))


def preprocess_data_samples(data_samples, stopwords):
    '''
        Main preprocessing function that
        runs _process in parallel for large
        documents.
        Arguments:
            data_samples: Data samples
            stopwords : list of stopwords
    '''

    pool = multiprocessing.Pool(multiprocessing.cpu_count() - 1)
    stopwords_regex = '|'.join(map(re.escape, stopwords))

    results = pool.map(
        _process, map(
            lambda sample: (
                sample, stopwords_regex), data_samples))

    return results


def build_stoplist(data_samples, most_common=100):
    '''
        Function to build topic-specific stoplists
    '''
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
    '''
        Split on camel-case
    '''
    matches = re.finditer(
        '.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)',
        identifier)
    return [m.group(0).lower() for m in matches]


def split_underscores(s):
    '''
        Split on underscores
    '''
    return s.split('_')


def remove_nonalpha(s):
    '''
        Remove non-alpha from string
    '''
    return ''.join([x for x in s if x.isalpha()])


def expand(s):
    '''
        Expand string on multiple expansion identifiers
        E.g. void(int) becomes ['void', 'int']
    '''
    expanders = ['(', ')', '{', '}', '[', ']', '%', '\n']
    return list(filter(lambda x: x != '', multi_split(expanders, s)))


def multi_split(delimiters, string, maxsplit=0):
    '''
        Split on multiple delimiters
    '''
    regexPattern = '|'.join(map(re.escape, delimiters))
    return re.split(regexPattern, string, maxsplit)


def pipelined_removals(
        s,
        pipeline=[
            expand,
            split_underscores,
            camel_case_split,
            wordninja.split],
        cleaner=remove_nonalpha):

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
    argparser = argparse.ArgumentParser(
        description='Generate Bag of Words embeddings')
    argparser.add_argument('-d', type=str, default='.', help='Directory')
    argparser.add_argument('-m', type=str, help='Modules')

    argparser.add_argument(
        '-o',
        type=str,
        help='Output File',
        default='embeddings.bow')

    args = argparser.parse_args()

    os.chdir(args.d)


    source_code_document_embeddings(
        ['.c', '.h'], modules=args.m, outfile=args.o)
