from graph import UndirectedGraph
from location import Location

def example_usage():
    # Create a new graph
    g = UndirectedGraph()

    # Define some location objects
    loc1 = Location(lat=40.7128, long=-74.0060, attr={"city": "New York"})
    loc2 = Location(lat=34.0522, long=-118.2437, attr={"city": "Los Angeles"})
    loc3 = Location(lat=41.8781, long=-87.6298, attr={"city": "Chicago"})

    # Add them to the graph
    g.add_location(loc1)
    g.add_location(loc2)
    g.add_location(loc3)

    # Link them with edges using some "distance" as the weight
    g.add_edge(loc1, loc2, weight=3940)  # e.g., distance in km
    g.add_edge(loc1, loc3, weight=1146)
    g.add_edge(loc2, loc3, weight=2815)

    # Print vertex weights (comes from the .get_weight() method)
    print("loc1 weight:", g.get_vertex_weight(loc1))
    print("loc2 weight:", g.get_vertex_weight(loc2))
    print("loc3 weight:", g.get_vertex_weight(loc3))

    # Print edges
    print("\nEdges in the graph:")
    for edge in g.edges():
        print(edge)

    # Example of changing an edge weight
    g.set_edge_weight(loc1, loc2, 4000)
    print("\nUpdated edge loc1-loc2:", g.get_edge_weight(loc1, loc2))

    # Remove an edge
    g.remove_edge(loc2, loc3)
    print("\nEdges after removing loc2-loc3:", g.edges())

    # Remove a vertex entirely
    g.remove_vertex(loc1)
    print("\nEdges after removing loc1:", g.edges())
    print("Remaining vertices:", g.vertices())


if __name__ == "__main__":
    example_usage()
