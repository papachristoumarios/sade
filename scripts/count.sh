#!/bin/bash
echo "Filename: $1"
echo "Number of nodes"
awk -v RS="[[:blank:]\t\n]+" '1' $1 | sort | uniq | wc -l
echo "Number of edges"
cat $1 | wc -l
