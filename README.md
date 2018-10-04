# SADE: Software Architecture with Document Embeddings

## What is SADE? 

TBA



## Installation 

Installing system/user-wide (with sudo if system-wide):

```bash
make install
```

Installing on a virtual environment using `virtualenv`:

```bash
make install_venv
```



## Toolkit

### Document Embeddings Generation with Gensim and spaCy

You can generate document embeddings using the doc2vec algorithm provided via gensim. The source code is initially preprocessed with spaCy with the following pipeline:

1. Stopword Removal
2. Tokenization
3. Lemmatization

Embeddings are generated from all .c and .h files to an output file (e.g. embeddings.bin)

#### Usage

```bash
embeddings.py -h
```



## References

TBA.

