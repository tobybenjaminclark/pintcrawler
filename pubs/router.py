from graph import UndirectedGraph

def get_all_routes_from_vertex(graph, start):
    """
    Given an undirected graph and a starting vertex,
    return all simple routes (paths) starting at that vertex.
    Each route is represented as a tuple (route, weight) where:
      - route: list of vertices
      - weight: the total weight of the route
    """
    def dfs(current, path, current_weight=0.0):
        # Record the current path as a valid route (with its cumulative weight).
        routes = [(path, current_weight)]
        # For each neighbor of the current vertex, if it is not already in the path, extend the route.
        for neighbor, weight in graph.get_neighbors(current):
            if neighbor not in path:
                new_weight = current_weight + weight
                routes.extend(dfs(neighbor, path + [neighbor], new_weight))
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
