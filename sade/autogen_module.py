# Automatically Generate Module Files in JSON format
# Usage: autogen_module.py -h
# Author: Marios Papachristou
import os
import argparse
import json
import sys
import sade.helpers
import collections


def gen_module_dict(depth=-1, inverse=False, suffix='.c'):
    """Generate a module mapping"""
    filelist = sade.helpers.list_files('.', suffix=suffix, recursive=True)
    if inverse:
        modules = collections.defaultdict(list)
    else:
        modules = {}

    for name in filelist:
        head, tail = sade.helpers.basename(
            name, depth=depth), sade.helpers.basename(name)
        # module maps to files
        if inverse:
            modules[head].append(tail)
        # file maps to module
        else:
            modules[tail] = head
    return modules


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        description='Autogenerate module files as and export to JSON')
    argparser.add_argument(
        '-d',
        type=int,
        default=1,
        help='Depth of generation')
    argparser.add_argument(
        '--inv',
        action='store_true',
        help='Generate Inverse Mapping')
    argparser.add_argument('--suffix', default='.c', help='File suffix')
    args = argparser.parse_args()

    modules = gen_module_dict(
        depth=-args.d,
        inverse=args.inv,
        suffix=args.suffix)

    # export to json
    print(json.dumps(modules, indent=4, separators=(',', ': ')))
