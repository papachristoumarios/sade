import argparse
from sade.helpers import cmd
from sade.autogen_module import *
import sys
import glob
import os
import collections
import numpy as np
import subprocess
import tabulate
from sade.metrics import silhouette_score

def get_argparser():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-r', default='/home/marios/workspace')
    argparser.add_argument('-p', default=0, type=int)
    argparser.add_argument('-d', default=-1, type=int)
    argparser.add_argument('-o', default='sade/results')
    argparser.add_argument('--clean', action='store_true')
    return argparser

def get_ground_truth(modules, p=0):
    mapping = collections.defaultdict(set)

    for val in modules.values():
            ground = val.split('/')[p]
            mapping[ground] |= {val}

    return mapping

def get_clustering_stats(bunch):

    with open(bunch) as f:
        lines = f.read().splitlines()

    sizes = []

    for line in lines:
        name, files = line.split('= ')
        files = files.split(', ')
        sizes.append(len(files))

    return np.array(sizes)

def clean():
    os.system('rm -rf *.bin *.bunch')

def export_ground_truth(mapping):
    result = []
    for i, (key, val) in enumerate(mapping.items()):
        result.append('{}= {}'.format(i, ', '.join(list(val))))

    return '\n'.join(result)

def get_metrics_table(tabular, name):

    result = '''\\begin{{table}}
\\centering
    {0}
\\caption{{ Clustering Results for {1}}}
\\label{{tab:{1}_metrics}}
\\end{{table}}'''.format(tabular, name)
    return result



PROJECTS = [
    ('postgres', 'postgres/src', 'call-graphs/call-graphs/postgres', -1),
    ('nginx', 'nginx/src', 'call-graphs/call-graphs/nginx', 0),
    ('apr', 'apr', 'call-graphs/call-graphs/apr', 0),
    ('apr-util', 'apr-util', 'call-graphs/call-graphs/apr-util', 0),
    ('lxc', 'lxc/src', 'call-graphs/call-graphs/lxc', 0),
    ('httpd', 'httpd', 'call-graphs/call-graphs/httpd', 0),
    ('vim', 'vim/src', 'call-graphs/call-graphs/vim', 0)
    # ('linux', 'linux', 'call-graphs/call-graphs/linux', -1)
]


if __name__ == '__main__':
    argparser = get_argparser()
    args = argparser.parse_args()

    os.chdir(args.r)


    for name, src, cgraphs_dir, depth in PROJECTS:
        cgraphs = glob.glob(os.path.join(args.r, cgraphs_dir, '*fgraph*'))
        os.chdir(src)

        print('Processing', name)
        print('Generating modules file')

        modules = gen_module_dict(
            depth=depth,
            inverse=False,
            suffix=['.c', '.h'])

        files = gen_file_dict(suffix=['.c', '.h'])

        print('Generate JSON')
        exported_json = export_module_file(modules, export_type='json')
        with open('modules.json', 'w+') as f:
            f.write(exported_json)

        print('Generate RSF')
        exported_rsf = export_module_file(modules, export_type='rsf')
        with open('modules.rsf', 'w+') as f:
            f.write(exported_rsf)

        print('Generate ground truth')
        ground_truth = get_ground_truth(modules)
        ground_truth_bunch = export_ground_truth(ground_truth)

        with open('ground.bunch', 'w+') as f:
            f.write(ground_truth_bunch)

        n_clusters = len(ground_truth)
        # import pdb; pdb.set_trace()

        print('Number of clusters', n_clusters)

        print('Train doc2vec embeddings')
        os.system('embeddings.py -m modules.json -d . -o embeddings.bin')

        print('Train BoW')
        os.system('bow.py -m modules.json -d . -o bow.bin')

        print('Baseline Clustering')
        os.system('clustering.py -e embeddings.bin -n {} -l ward --affinity euclidean>ward.bunch'.format(n_clusters))
        os.system('clustering.py -e embeddings.bin -n {} -l complete --affinity cosine>complete.bunch'.format(n_clusters))
        os.system('clustering.py -e embeddings.bin -n {} -l average --affinity cosine>average.bunch'.format(n_clusters))
        os.system('limbo.py -i bow.bin -n {} -B 10 >limbo.bunch'.format(n_clusters))

        print('Running SADE')
        for cgraph in cgraphs:
            cgraph_name = os.path.split(cgraph)[-1].split('.')[0].strip('_all')
            os.system('community_detection.py -e embeddings.bin -m modules.json -g {} >sade_{}.bunch'.format(cgraph, cgraph_name))
            # os.system('community_detection.py -e embeddings.bin -m modules.json -g {} --directed >sade_directed_{}.bunch'.format(cgraph, cgraph_name))

        print('Generating Visualizations')
        #
        bunches = glob.glob('*.bunch')

        for cgraph in cgraphs:
            for bunch in bunches:
                os.system('visualize_graphs.py -m modules.json -e embeddings.bin -g {} -b {} --method spectral -s {}'.format(cgraph, bunch, name))


        os.system('visualize_radar.py --outer ground.bunch -e embeddings.bin -s {} --inner {}'.format(name, ' --inner '.join(bunches)))

        headers = ['Method', '\\# Clusters', 'Size Range', '$\\bar x$', '$\\sigma$', 'Median', 'Sihlouette Score', 'MoJo']
        results = []

        for bunch in bunches:
            bunch_name = os.path.split(bunch)[-1].replace('_', ' ').split('.')[0]

            mojo = int(subprocess.check_output(['java', 'MoJo', bunch, 'ground.bunch']).decode('utf-8').strip('\n'))

            stats = get_clustering_stats(bunch)

            results.append([
                '\\textsc{{{}}}'.format(bunch_name.lower()),
                len(stats),
                '{}--{}'.format(stats.min(), stats.max()),
                round(stats.mean(), 1),
                round(stats.std(), 1),
                round(np.median(stats), 1),
                round(silhouette_score(bunch, 'embeddings.bin'), 4),
                mojo
            ])

        ''' Sort by MoJo distance '''
        results = list(sorted(results, key=lambda x: -x[-1]))

        tabulate.LATEX_ESCAPE_RULES = {}

        tabular = tabulate.tabulate(results, headers, tablefmt='latex_booktabs')

        table = get_metrics_table(tabular, name)

        with open('{}_clustering_results.tex'.format(name), 'w+') as f:
            f.write(table)

        os.chdir(args.r)
