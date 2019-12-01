#!/bin/bash

# Author : Marios Papachristou
# Get call graphs using Cscout's REST API

# Loop until cscout is available
#until $(curl --output /dev/null --silent --head --fail http://localhost:8081/); do
#	sleep 50
#done

# File include graph
curl -X GET "http://localhost:8081/fgraph.txt?gtype=I&all=1" > fgraph_I_all.txt

# Compile-time dep graph
curl -X GET "http://localhost:8081/fgraph.txt?gtype=C&all=1" > fgraph_C_all.txt

# Control dependency graph (through fcn calls) 
curl -X GET "http://localhost:8081/fgraph.txt?gtype=F&n=D&all=1" > fgraph_F_D_all.txt

# Data dependency graph (through globals) 
curl -X GET "http://localhost:8081/fgraph.txt?gtype=G&all=1" > fgraph_G_all.txt

# Cummulative metrics
curl -X GET "http://localhost:8081/funmetrics.html" > metrics.txt

# Call graph (functions) 
curl -X GET "http://localhost:8081/cgraph.txt" > cgraph.txt

# Call graph (with macros)
curl -X GET "http://localhost:8081/cgraph.txt?all=1" > cgraph_all.txt 
