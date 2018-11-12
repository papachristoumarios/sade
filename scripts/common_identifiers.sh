#!/bin/bash
# Find common identifiers in .c and .h files
# Author: Marios Papachristou

find . -type f -name *.[c\|h] |
xargs -n $(find . -type f -name *.[c\|h] | wc -l) cat |
tr -c 'A-Za-z' \\n |
sort |
uniq -c |
sort -rn |
head -1000
