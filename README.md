# SADE: Software Architecture with Document Embeddings

## What is SADE? 

SADE (abbreviated as Software Architecture with Document Embeddings) is a library for studying and recovering the architectures of complex softwares systems. Our approach uses a combination of document embeddings on the source code provided by **Doc2Vec** as well as the existing structure of the codebase via the call graph. Document embeddings have never been used before to study the architecture of a software system. We will construct a geometric graph on a metric space and iteratively and form communities in this graph ariving at a layered architecture viewed from the call graph perspective. It has been applied on the Linux Kernel codebase and will be compared to its existing layered architecture using **MoJo** distance as a clusterings metric as well as, compare its stability and extremity compared to other Software Clustering. 

The software is released under the MIT License. 

## Installation 

Installing system/user-wide (with sudo if system-wide):

```bash
make install
```

Installing on a virtual environment using `virtualenv`:

```bash
make install_venv
```



## Technologies Used

SADE was developed in Python 3.x using the following libraries:

* Gensim
* spaCy
* sklearn
* NetworkX





## Toolkit

### Document Embeddings Generation with Gensim and spaCy

You can generate document embeddings using the doc2vec algorithm provided via gensim. The source code is initially preprocessed with spaCy with the following pipeline:

1. Stop-word Removal
2. Tokenization
3. Lemmatization

Embeddings are generated from all .c and .h files to an output file (e.g. embeddings.bin)

#### Usage

```bash
embeddings.py -h
```



## References

TBA.

