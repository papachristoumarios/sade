#!/bin/bash

# Author : Marios Papachristou
# Get call graphs using Cscout's REST API

PORT=$1
DEST=$2

# Loop until cscout is available
#until $(curl --output /dev/null --silent --head --fail http://localhost:$PORT/); do
#	sleep 50
#done

mkdir -p $DEST

# File include graph
curl -X GET "http://localhost:$PORT/fgraph.txt?gtype=I&all=1" > $DEST/fgraph_I_all.txt

# Compile-time dep graph
curl -X GET "http://localhost:$PORT/fgraph.txt?gtype=C&all=1" > $DEST/fgraph_C_all.txt

# Control dependency graph (through fcn calls) 
curl -X GET "http://localhost:$PORT/fgraph.txt?gtype=F&n=D&all=1" > $DEST/fgraph_F_D_all.txt

# Data dependency graph (through globals) 
curl -X GET "http://localhost:$PORT/fgraph.txt?gtype=G&all=1" > $DEST/fgraph_G_all.txt

# Cummulative metrics
curl -X GET "http://localhost:$PORT/funmetrics.html" > $DEST/metrics.txt

# Call graph (functions) 
curl -X GET "http://localhost:$PORT/cgraph.txt" > $DEST/cgraph.txt

# Call graph (with macros)
curl -X GET "http://localhost:$PORT/cgraph.txt?all=1" > $DEST/cgraph_all.txt 
