from graph import UndirectedGraph

def get_all_routes_from_vertex(graph, start):
    """
    Given an undirected graph and a starting vertex,
    return all simple routes (paths) starting at that vertex.
    Each route is represented as a list of vertices.
    """
    def dfs(current, path):
        # Record the current path as a valid route.
        routes = [path]
        # Iterate over all neighbors of the current vertex.
        for neighbor, _ in graph.get_neighbors(current):
            # Only extend the path if we haven't visited this neighbor yet.
            if neighbor not in path:
                routes.extend(dfs(neighbor, path + [neighbor]))
        return routes

    return dfs(start, [start])


def get_all_routes(graph):
    """
    For each vertex in the graph, compute all routes starting from that vertex.
    Returns a dictionary mapping each starting vertex to the list of its routes.
    """
    all_routes = {}
    for vertex in graph.vertices():
        all_routes[vertex] = get_all_routes_from_vertex(graph, vertex)
    return all_routes
