from graph import UndirectedGraph
from location import Location


EDGE_WEIGHT = 1


def get_vertex_weight(current: Location) -> float:
    # we say that pubs < 2.5 stars are shit
    return current.attr["rating"]


def get_all_routes_from_vertex(graph, start):
    """
    Given an undirected graph and a starting vertex,
    return all simple routes (paths) starting at that vertex that contain
    between 3 and 5 pubs (inclusive).
    Each route is represented as a tuple (route, weight) where:
      - route: list of vertices
      - weight: the total weight of the route
    """

    def dfs(current, path, current_weight=0.0):
        routes = []
        path_length = len(path)

        # If the path has between 3 and 5 vertices, record it.
        if 3 <= path_length <= 5:
            routes.append((path, current_weight))

        # If we have reached 5 pubs, do not extend further.
        if path_length == 5:
            return routes

        # Try extending the path.
        for neighbor, edge_cost in graph.get_neighbors(current):
            if neighbor not in path:
                # Update the weight: subtract the edge cost (scaled) and add the current vertex's weight.
                new_weight = current_weight - (edge_cost * EDGE_WEIGHT) + get_vertex_weight(current)
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
        gl_routes = []

    return all_routes
