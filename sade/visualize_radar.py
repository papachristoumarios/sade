import numpy as np
import argparse
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
from sade.community_detection import load_data, angle_similarity, corr_coeff
import collections


def radar_factory(num_vars, frame='circle'):
    """Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle' | 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

    class RadarAxes(PolarAxes):

        name = 'radar'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

        def draw(self, renderer):
            """ Draw. If frame is polygon, make gridlines polygon-shaped """
            if frame == 'polygon':
                gridlines = self.yaxis.get_gridlines()
                for gl in gridlines:
                    gl.get_path()._interpolation_steps = num_vars
            super().draw(renderer)


        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                    + self.transAxes)


                return {'polar': spine}
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta

def load_clusters(bunchfile, model):
    clusters = collections.defaultdict(list)

    with open(bunchfile) as f:
        lines = f.read().splitlines()

    for line in lines:
        name, files = line.split('= ')
        files = files.split(', ')
        try:
            name = int(name)
        except:
            pass
        for filename in files:
            clusters[name].append(model.docvecs[filename])

    for key, val in clusters.items():
        clusters[key] = np.array(val).mean(0)

    return clusters

def compute_correlations(inner_clusters, outer_clusters):
    corr = {}

    for outer_key, outer_val in outer_clusters.items():
        maximum = (None, -1)
        for inner_key, inner_val in inner_clusters.items():
            cc = corr_coeff(outer_val, inner_val)
            if cc > maximum[1]:
                maximum = (inner_key, cc)
        corr[outer_key] = maximum

    return corr

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--outer', default='ground.bunch')
    argparser.add_argument('--inner', action='append')
    argparser.add_argument('-l', help='Ground truth labels')
    argparser.add_argument('-o', default='.')
    argparser.add_argument('-e', default='embeddings.bin', help='Doc2vec model')
    # argparser.add_argument('-b', help='Bunchfile')
    argparser.add_argument('-s', help='System name')
    args = argparser.parse_args()

    X, y, model = load_data(args.e)

    results = []
    outer_clusters = load_clusters(args.outer, model)
    legend = []

    for inner_bunch in args.inner:
        if inner_bunch == 'ground.bunch':
            continue
        inner_clusters = load_clusters(inner_bunch, model)
        correlations = compute_correlations(inner_clusters, outer_clusters)
        results.append(correlations)
        legend.append(os.path.split(inner_bunch)[-1].split('.')[0])

    labels = list(sorted(results[0].keys()))
    values = []


    for result in results:
        temp = []
        for label in labels:
            temp.append(result[label][1])
        values.append(temp)


    data = [labels, (args.s, values)]

    N = len(data[0])
    theta = radar_factory(N, frame='polygon')

    spoke_labels = data.pop(0)
    title, case_data = data[0]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(top=0.85, bottom=0.05)

    ax.set_rgrids(0.1 * np.arange(10))
    ax.set_title(title,  position=(0.5, 1.1), ha='center')

    for i, d in enumerate(case_data):
        line = ax.plot(theta, d, label=legend[i])
        ax.fill(theta, d,  alpha=0.25)
    ax.set_varlabels(spoke_labels)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 0),
          fancybox=True, ncol=5)
    plt.savefig(os.path.join(args.o, 'radar_{}.png'.format(args.s)), format='png')
