#!/bin/bash
# Find common identifiers in .c and .h files
# Author: Marios Papachristou


find . -type f -name "*.[c\|h]" |
xargs cat |
tr -c 'A-Za-z' \\n |
sort |
uniq -c |
sort -rn |
head -$1
