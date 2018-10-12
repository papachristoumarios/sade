import networkx as nx
import sade.violation_metrics

def test_bcvi():
	G = nx.DiGraph()
	G.add_edges_from([(0,1), (1,2), (2,1), (2, 0)])
	layers = {0 : 0, 1: 1, 2: 2}
	assert(sade.violation_metrics.back_call_violation_index(G, layers) ==  {0: 1.0, 1: 1.0, 2: 0.0})
	assert(sade.violation_metrics.skip_call_violation_index(G, layers) == {0: 0.0, 1: 0.0, 2: 0.5})

test_bcvi()

