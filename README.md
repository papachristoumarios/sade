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



## Usage 

With SADE you can analyze your C project using the components provided by it. Below there are steps on how you should do it. We will be using [CScout](https://github.com/dspinellis/cscout) for Static Graph Analysis. 



### Step 1: Generate Module Definition File

For defining the modules of the system, each file must map to a module. You should generate a `modules.json` file with the following format:

```json
{
    "boo.c" : "boomodule",
    "foo.c" : "foomodule"
}
```

You can do this manually, but in case the project is strictly organized into modules (as directories) you can use the `autogen_module` tool to generate the module definition. You can do this by:

```bash
autogen_module.py -d 1
```

where the `-d` specifies the depth that the modules must be split. An example is located at `examples/linux/modules.json`.



### Step 2: Generate document embeddings

After creating the `modules.json` definitions file you can proceed generating the Doc2Vec using Gensim and spaCy preprocessed with the following pipeline:

1. Stop-word Removal
2. Tokenization
3. Lemmatization

You can generate the embeddings with the `embeddings.py` script using

```bash
embeddings.py -m modules.json -o embeddings.bin -p params.json
```

You can configure it further by passing parameters for the model with `-p` flag as a `params.json` file. 

A `params.json` file example:

```json
{
    'size': 200, 
    'window': 10, 
    'min_count': 10,
    'workers':7, 
    'sample': 1E-3
}
```



### Step 3: Generating the Call Graph through CScout

Generate the `make.cs` file via:

```bash
csmake
```

in case you have a multi-core machine you can use the classic `-j` flag:

```bash
csmake -j7
```

After generating the `make.cs` file you can analyze it with CScout via

```bash
cscout make.cs
```

CScout may complain for undefined names. What you can to is to place their respective definitions to `cscout-pre-defs.h` (before `csmake`) and to `cscout-post-defs.h`. For more information on it, please refer to [CScout Documentation](https://www2.dmst.aueb.gr/dds/cscout/doc). 

An example of such configuration for the Linux Kernel 4.x Codebase is located at `examples/linux` . 

Finally, you can send `GET` requests to CScout and get responses through its REST API. 

For example:

```bash
# Call graph (functions) 
curl -X GET "http://localhost:8081/cgraph.txt" >graph.txt
```

You can get all the call graphs via running `scripts/get_graphs_rest.sh`. 



#### Pre-generated call graph for Linux Kernel 4.21

A pre-generated call graph of Linux Kernel 4.21 (20.1 million lines of source code) can be found [here](https://pithos.okeanos.grnet.gr/public/qJajffcQ7qEQwqXNrKkAW5). The call graphs come to a format:

```
u1 v1
u2 v2 
// more edges
un vn
```

where `ui vi` is a directed edge from `ui` to `vi`. 

The call graph was generated on an Intel(R) Xeon(R) CPU E5-1410 0 @ 2.80GHz with 72G of RAM. 



### Step 4: Getting the layers configuration

After generating the embeddings you can use the `layerize.py` tool to get the proposed layered architecture. You can do it by:

```bash
layerize.py -e embeddings.bin -g graph.txt >layers.bunch
```

to export it to a `.bunch` file. The format of a bunch file is:

```
Layer0= File1, File2, File3
```

or to JSON with:

```bash
layerize.py -e embeddings.bin -g graph.txt --export json >layers.json
```



### Step 5 (Optional) : Evaluation of Results

#### Authoritativeness - Comparing to Ground Truth

Once generating the layered architecture, in case there is an existing one serving as ground truth, such that the Linux Layers located at `examples/linux/ground_truth.json` you can compare the architectures with the MoJoFM metric provided in the `mojo` package via:

```python
import mojo
mojo.mojo('proposed_layers.bunch', 'ground_truth.bunch', '-fm')
```



## Technologies Used

SADE was developed in Python 3.x using the following libraries:

* Gensim
* spaCy
* sklearn
* NetworkX



## Toolkit

### Document Embeddings Generation with Gensim and spaCy

Embeddings are generated from all .c and .h files to an output file (e.g. embeddings.bin)

#### Usage

```bash
embeddings.py -h
```



## Citing the Project 

 