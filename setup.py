"""Setup module"""
from setuptools import setup

setup(
    name='sade',
    version='1.0',
    description='Software Architecture with Document Embeddings',
    author='Marios Papachristou',
    author_email='adityag@cs.stanford.edu ',
    url='https://github.com/aditya-grover/node2vec',
    packages=['node2vec'],
    package_dir={'node2vec': 'node2vec'},
    scripts=['node2vec/train_node2vec.py'])
