# Count C Source Code Files
# Author: Marios Papachristou
# Usage: ./count_sloc.sh /path/to/repo

DEST=$1

find $DEST -name '*.h' -o -name '*.c' | xargs cat | wc -l
