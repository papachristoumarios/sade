import sade.helpers
import argparse
import collections
import json

def generate_ground_truth(modules_json, prefixes_json):
    with open(modules_json) as f:
        modules = json.loads(f.read())
    with open(prefixes_json) as f:
        prefixes = json.loads(f.read())

    ground_truth = collections.defaultdict(list)

    for module in modules.values():
        temp_layer = -1
        for prefix, layer in prefixes.items():
            if module.startswith(prefix):
                temp_layer = layer

        ground_truth[temp_layer].append(module)

    return ground_truth

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(usage='Ground Truth Generator for Linux')
    argparser.add_argument('-m', help='Modules file')
    argparser.add_argument('-p', help='Prefixes')
    argparser.add_argument('--export', help='Export type', default='bunch')
    args = argparser.parse_args()

    ground_truth = generate_ground_truth(args.m, args.p)

    if args.export == 'bunch':
        print(sade.helpers.generate_bunch(ground_truth))
    elif args.export == 'json':
        print(json.dumps(ground_truth))
