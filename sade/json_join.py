# Join JSON Files describing architecture using a Hash Join
# Join runs linear in time since the inputs are hashtables
# Usage: json_join.py -h
# Author: Marios Papachristou

import json
import argparse
import collections
import os
import sys


def join_dicts(layers, modules, inverse=False):
    # Hash-Join Implementation
    if inverse:
        result = collections.defaultdict(list)
    else:
        result = {}

    for filename, module in modules.items():
        try:
            if not inverse:
                result[filename] = layers[module]
            else:
                result[layers[module]].append(filename)
        except KeyError:
            sys.stderr.write(
                'Module {} is not part of any layer\n'.format(filename))
    return result


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '-m',
        help='Module JSON file',
        default='modules.json')
    argparser.add_argument(
        '-l',
        help='Layers JSON file',
        default='layers.json')
    argparser.add_argument('--inv', help='Invert mapping', action='store_true')
    args = argparser.parse_args()

    layers = json.loads(open(args.l).read())
    modules = json.loads(open(args.m).read())

    joined = join_dicts(layers, modules, inverse=args.inv)

    # export to json
    print(json.dumps(joined, indent=4, separators=(',', ': ')))
