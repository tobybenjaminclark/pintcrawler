import matplotlib

from graph import UndirectedGraph
from location import Location
import networkx as nx

import matplotlib.pyplot as plt
matplotlib.use("TkAgg")   # or "Qt5Agg", "MacOSX", etc.

def visualize_graph(graph):
    """Convert the UndirectedGraph into a NetworkX graph and display it with pub names as node labels."""
    
    nx_graph = nx.Graph()

    # Add nodes with pub names as labels
    for vertex in graph.vertices():
        # Assuming vertex is an instance of Location that has a 'name' attribute
        nx_graph.add_node(vertex, label=vertex.attr['name'])

    # Add edges (with weights, assuming weight is stored in the edge)
    for (v1, v2, w) in graph.edges():
        nx_graph.add_edge(v1, v2, weight=w)

    # Basic spring layout for node positioning
    pos = nx.spring_layout(nx_graph)

    # Draw the nodes and edges
    nx.draw_networkx_nodes(nx_graph, pos, node_size=500, node_color='lightblue')
    nx.draw_networkx_edges(nx_graph, pos, width=1.0, alpha=0.5)

    # Draw node labels (pub names)
    labels = nx.get_node_attributes(nx_graph, 'label')
    nx.draw_networkx_labels(nx_graph, pos, labels=labels, font_size=10, font_color='black')

    # Draw edge weights if necessary
    edge_labels = {(u, v): d["weight"] for u, v, d in nx_graph.edges(data=True)}
    nx.draw_networkx_edge_labels(nx_graph, pos, edge_labels=edge_labels)

    # Title and display
    plt.title("Pub Network Visualization")
    plt.axis("off")  # Hide the axis
    plt.show()