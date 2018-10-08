import mojo
import matplotlib.pyplot as plt
import networkx as nx
import random
import collections

def sca_stability(S, K, cluster_fcn, mode='-m+', plot=True, **args):

    initial_partition = cluster_fcn(S)
    mojo.generate_bunch(initial_partition, 'initial.bunch')

    distances = []
    counter = 0
    N = len(S.nodes())
    for j in range(K):
        delete_edges_count = int(0.001 * N)
        delete_nodes_count = int(0.0025 * N)

        # delete edges and nodes
        deleted_edges = random.sample(S.edges(), delete_edges_count)
        for e in deleted_edges:
            S.remove_edge(*e)

        deleted_nodes = random.sample(list(S.nodes()), delete_nodes_count)

        #
        # for n in deleted_nodes:
        #     S.remove_node(n)


        # add edges
        add_edges_count = int(0.005 * N)

        connect_nodes_count =  int(0.0025 * N)

        for i in range(add_edges_count):
            u = random.getrandbits(64)
            G.add_node(u)
            if connect_nodes_count > 0:
                v = random.choice(list(S.nodes()))
                G.add_edge(u, v)
                connect_nodes_count -= 1

        partition = cluster_fcn(S)

        mojo.generate_bunch(partition, 'partition-{}.bunch'.format(j))

        m = mojo.mojo('initial.bunch', 'partition-{}.bunch'.format(j), mode)
        distances.append(m)


        assert(m != None)

        if m <= N // 100:
            counter += 1

    if plot == True:

        plt.plot(range(K), distances)
        plt.title('Clustering Stability')
        plt.show()

    return counter / K * 100

def dummy_cluster_fcn(S):

    N = len(S.nodes())
    K = 5
    dummy_partition = collections.defaultdict(list)

    for n in S.nodes():
        cl = random.randint(1, K)
        dummy_partition[cl].append(n)

    return dummy_partition

def test_stability():
    G = nx.complete_graph(2000)
    print(sca_stability(G, 2, dummy_cluster_fcn))
