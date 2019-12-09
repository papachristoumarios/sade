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
        _, tail = os.path.split(name)
        head = name.lstrip('./')
        for i in range(abs(depth)):
            head, _ = os.path.split(head)

        # module maps to files
        if inverse:
            modules[head].append(tail)
        # file maps to module
        else:
            modules[tail] = head
    return modules

def export_module_file(modules, export_type):
    # Export JSON (suitable for most experiments)
    if export_type == 'json':
        return json.dumps(modules, indent=4, separators=(',', ': '))
    # Export rsf file for clustering with ACDC
    elif export_type == 'rsf':
        memberships = []

        for child, parent in modules.items():
            if parent == '' or child == '':
                continue
            memberships.append('depends {} {}'.format(child, parent))

        return '\n'.join(memberships)

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
    argparser.add_argument('--export', default='json', help='Export filetype')
    args = argparser.parse_args()

    modules = gen_module_dict(
        depth=-args.d,
        inverse=args.inv,
        suffix=args.suffix)

    # export to json
    exported = export_module_file(modules, export_type=args.export)
    print(exported)
