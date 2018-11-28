# Automatically Generate Module Files in JSON format
# Usage: autogen_module.py -h
# Author: Marios Papachristou
import os
import argparse
import json
import sys
import sade.helpers
import collections


def gen_module_dict(depth=-1, inverse=False, suffix=['.c', '.h']):
    """Generate a module mapping"""
    filelist = []
    for s in suffix:
        filelist.extend(sade.helpers.list_files('.', suffix=s, recursive=True))

    if inverse:
        modules = collections.defaultdict(list)
    else:
        modules = {}

    for name in filelist:
        splitted = os.path.split(name)
        head, tail = splitted[0].strip('./'), splitted[1]
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
    argparser.add_argument('--suffix', action='append', help='File suffix')
    args = argparser.parse_args()

    modules = gen_module_dict(
        depth=-args.d,
        inverse=args.inv,
        suffix=args.suffix)

    # export to json
    print(json.dumps(modules, indent=4, separators=(',', ': ')))
