class UndirectedGraph:
    """
    A simple undirected graph implementation that supports
    vertex weights and edge weights.

    Internally, the graph is stored as an adjacency list (dict).
    Each key in the adjacency list is a vertex, and the value is
    a list of tuples (neighbor, edge_weight).
    """

    def __init__(self):
        # Dictionary mapping vertex -> list of (neighbor, edge_weight)
        self.adjacency_list = {}

        # Dictionary to store vertex -> vertex_weight
        self.vertex_weights = {}

    def add_vertex(self, vertex, weight=0):
        """
        Add a vertex to the graph with an optional weight (default=0).
        """
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []
            self.vertex_weights[vertex] = weight
        else:
            # If the vertex already exists, optionally update its weight
            self.vertex_weights[vertex] = weight

    def add_edge(self, v1, v2, weight=0):
        """
        Add a bidirectional (undirected) edge between v1 and v2
        with an optional edge weight (default=0).

        If v1 or v2 does not exist yet, it is created with a
        default vertex weight of 0.
        """
        if v1 not in self.adjacency_list:
            self.add_vertex(v1, 0)
        if v2 not in self.adjacency_list:
            self.add_vertex(v2, 0)

        # Add edge in both directions for an undirected graph
        self.adjacency_list[v1].append((v2, weight))
        self.adjacency_list[v2].append((v1, weight))

    def get_vertex_weight(self, vertex):
        """
        Return the weight of the specified vertex.
        Raises KeyError if the vertex doesn't exist.
        """
        return self.vertex_weights[vertex]

    def set_vertex_weight(self, vertex, weight):
        """
        Update the weight of the specified vertex.
        Raises KeyError if the vertex doesn't exist.
        """
        if vertex not in self.vertex_weights:
            raise KeyError(f"Vertex {vertex} does not exist in the graph.")
        self.vertex_weights[vertex] = weight

    def get_neighbors(self, vertex):
        """
        Return a list of (neighbor, edge_weight) for the given vertex.
        Raises KeyError if the vertex doesn't exist.
        """
        return self.adjacency_list[vertex]

    def get_edge_weight(self, v1, v2):
        """
        Return the weight of the edge (v1, v2).
        If multiple edges exist between the same vertices, returns the
        first match. Raises a KeyError if v1 or v2 doesn't exist,
        or a ValueError if there is no edge between v1 and v2.
        """
        if v1 not in self.adjacency_list or v2 not in self.adjacency_list:
            raise KeyError(f"One or both vertices {v1}, {v2} do not exist.")

        for neighbor, w in self.adjacency_list[v1]:
            if neighbor == v2:
                return w
        # If we don't find the edge
        raise ValueError(f"No edge found between {v1} and {v2}.")

    def set_edge_weight(self, v1, v2, new_weight):
        """
        Update the weight of the edge (v1, v2) (and symmetrically (v2, v1)).
        Raises KeyError if v1 or v2 doesn't exist.
        Raises ValueError if there is no edge between v1 and v2.
        """
        if v1 not in self.adjacency_list or v2 not in self.adjacency_list:
            raise KeyError(f"One or both vertices {v1}, {v2} do not exist.")

        # Update edge v1->v2
        edge_found = False
        for i, (neighbor, w) in enumerate(self.adjacency_list[v1]):
            if neighbor == v2:
                self.adjacency_list[v1][i] = (neighbor, new_weight)
                edge_found = True
                break

        # Update edge v2->v1
        for i, (neighbor, w) in enumerate(self.adjacency_list[v2]):
            if neighbor == v1:
                self.adjacency_list[v2][i] = (neighbor, new_weight)
                break

        if not edge_found:
            raise ValueError(f"No edge found between {v1} and {v2}.")

    def remove_vertex(self, vertex):
        """
        Remove a vertex and all edges connected to it.
        Raises KeyError if the vertex does not exist.
        """
        if vertex not in self.adjacency_list:
            raise KeyError(f"Vertex {vertex} does not exist in the graph.")

        # Remove this vertex from other adjacency lists
        for nbr, _ in list(self.adjacency_list[vertex]):
            self.adjacency_list[nbr] = [(v, w) for (v, w) in self.adjacency_list[nbr] if v != vertex]

        # Finally, remove the vertex itself
        del self.adjacency_list[vertex]
        del self.vertex_weights[vertex]

    def remove_edge(self, v1, v2):
        """
        Remove the undirected edge between v1 and v2.
        Raises KeyError if v1 or v2 doesn't exist.
        Does nothing if the edge doesn't exist.
        """
        if v1 not in self.adjacency_list or v2 not in self.adjacency_list:
            raise KeyError(f"One or both vertices {v1}, {v2} do not exist.")

        # Remove from adjacency list for v1
        self.adjacency_list[v1] = [(nbr, w) for (nbr, w) in self.adjacency_list[v1] if nbr != v2]

        # Remove from adjacency list for v2
        self.adjacency_list[v2] = [(nbr, w) for (nbr, w) in self.adjacency_list[v2] if nbr != v1]

    def vertices(self):
        """
        Return a list of vertices in the graph.
        """
        return list(self.adjacency_list.keys())

    def edges(self):
        """
        Return a list of edges in the graph as (v1, v2, weight).
        Since the graph is undirected, (v1, v2) appears only once
        (with v1 < v2 if they are comparable).
        """
        visited = set()
        edge_list = []
        for v1 in self.adjacency_list:
            for (v2, w) in self.adjacency_list[v1]:
                if (v2, v1) not in visited:
                    visited.add((v1, v2))
                    visited.add((v2, v1))
                    edge_list.append((v1, v2, w))
        return edge_list


def example_usage():
    """
    Demonstrate how to use the UndirectedGraph class.
    """
    # Create a new graph
    g = UndirectedGraph()

    # Add vertices with weights
    g.add_vertex("A", weight=5)
    g.add_vertex("B", weight=2)
    g.add_vertex("C", weight=3)

    # Add edges with weights
    g.add_edge("A", "B", weight=10)
    g.add_edge("A", "C", weight=1)
    g.add_edge("B", "C", weight=2)

    # Print vertex weights
    print("Vertex A weight:", g.get_vertex_weight("A"))
    print("Vertex B weight:", g.get_vertex_weight("B"))
    print("Vertex C weight:", g.get_vertex_weight("C"))

    # Print edges
    print("\nEdges in the graph:", g.edges())

    # Update a vertex weight
    g.set_vertex_weight("A", 6)
    print("\nUpdated vertex A weight:", g.get_vertex_weight("A"))

    # Update an edge weight
    g.set_edge_weight("A", "B", 15)
    print("\nUpdated edges in the graph:", g.edges())

    # Remove an edge
    g.remove_edge("A", "C")
    print("\nEdges after removing A-C:", g.edges())

    # Remove a vertex
    g.remove_vertex("B")
    print("\nEdges after removing vertex B:", g.edges())
    print("Vertices left:", g.vertices())


if __name__ == "__main__":
    example_usage()
