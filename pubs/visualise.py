import matplotlib
from graph import UndirectedGraph
from location import Location
import networkx as nx
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")   # or "Qt5Agg", "MacOSX", etc.

def visualize_graph(graph):
    """Convert the UndirectedGraph into a NetworkX graph and display it with pub names as node labels, using latitude and longitude."""
    
    nx_graph = nx.Graph()

    # Add nodes with pub names as labels
    pos = {}  # Dictionary to store positions based on latitude and longitude
    latitudes = []
    longitudes = []

    for vertex in graph.vertices():
        # Assuming vertex is an instance of Location with 'latitude', 'longitude', and 'name' attributes
        latitudes.append(vertex.latitude)
        longitudes.append(vertex.longitude)
        nx_graph.add_node(vertex, label=vertex.name)

    # Normalize latitude and longitude to fit in a 2D space
    lat_min, lat_max = min(latitudes), max(latitudes)
    long_min, long_max = min(longitudes), max(longitudes)
    
    lat_range = lat_max - lat_min
    long_range = long_max - long_min

    # Normalize the positions
    for vertex in graph.vertices():
        lat_norm = (vertex.latitude - lat_min) / lat_range
        long_norm = (vertex.longitude - long_min) / long_range
        pos[vertex] = (long_norm, lat_norm)  # x = normalized longitude, y = normalized latitude

    # Add edges (with weights, assuming weight is stored in the edge)
    for (v1, v2, w) in graph.edges():
        nx_graph.add_edge(v1, v2, weight=w)

    # Draw the nodes and edges using the normalized positions
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
