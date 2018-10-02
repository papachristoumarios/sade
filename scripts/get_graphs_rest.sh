#!/bin/bash

# Author : Marios Papachristou
# Get call graphs using Cscout's REST API

# File include graph
curl -X GET "http://localhost:8081/fgraph.txt?gtype=I&all=1" > fgraph_I_all.txt

# Compile-time dep graph
curl -X GET "http://localhost:8081/fgraph.txt?gtype=C" > fgraph_C.txt

# Control dependency graph (through fcn calls) 
curl -X GET "http://localhost:8081/fgraph.txt?gtype=F&n=D" > fgraph_F_D.txt

# Data dependency graph (through globals) 
curl -X GET "http://localhost:8081/fgraph.txt?gtype=G" > fgrahp_G.txt

# Cummulative metrics
curl -X GET "http://localhost:8081/funmetrics.html" > metrics.txt

# Call graph (functions) 
curl -X GET "http://localhost:8081/cgraph.txt" > cgraph.txt

# Call graph (with macros)
curl -X GET "http://localhost:8081/cgraph.txt?all=1" > cgraph_all.txt 
