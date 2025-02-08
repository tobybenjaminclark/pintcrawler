import matplotlib

from graph import UndirectedGraph
from location import Location
import networkx as nx

import matplotlib.pyplot as plt
matplotlib.use("TkAgg")   # or "Qt5Agg", "MacOSX", etc.



def visualize_graph(graph):
    """Convert the UndirectedGraph into a NetworkX graph and display it."""
    import networkx as nx
    import matplotlib.pyplot as plt

    nx_graph = nx.Graph()

    # Add nodes
    for vertex in graph.vertices():
        nx_graph.add_node(vertex)

    # Add edges (with weights)
    for (v1, v2, w) in graph.edges():
        nx_graph.add_edge(v1, v2, weight=w)

    # Basic spring layout
    pos = nx.spring_layout(nx_graph)
    nx.draw_networkx(nx_graph, pos=pos, with_labels=True)

    # Draw edge weights
    edge_labels = {(u, v): d["weight"] for u, v, d in nx_graph.edges(data=True)}
    nx.draw_networkx_edge_labels(nx_graph, pos=pos, edge_labels=edge_labels)

    plt.title("UndirectedGraph Visualization")
    plt.axis("off")
    plt.show()
