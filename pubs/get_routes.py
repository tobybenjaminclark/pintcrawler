import datetime
import json
import googlemaps
from geopy.distance import geodesic
from concurrent.futures import ThreadPoolExecutor
from get_pubs import PubData, get_pubs, normalize_pub_ratings
from api_key import API_KEY
from graph import UndirectedGraph
from location import Location
from route import Pub, Route
from visualise import visualize_graph
from router import get_all_routes
import re
import math

gmaps = googlemaps.Client(key=API_KEY)

MAX_PUBS = 6

def get_nearest_pubs(pub: PubData, pubs: list[PubData], n: int = 5) -> list[PubData]:
    distances = [(geodesic((pub.latitude, pub.longitude), (other_pub.latitude, other_pub.longitude)).km, other_pub)
                 for other_pub in pubs if other_pub != pub]
    distances.sort(key=lambda x: x[0])
    return [other_pub for _, other_pub in distances[:n]]


def get_route_coordinates(route) -> list:
    """
    Extracts the route coordinates from the directions response.
    
    Args:
    - route: The directions response (from gmaps.directions).

    Returns:
    - A list of (lat, lng) tuples representing the route.
    """
    route_coordinates = []
    for step in route['legs'][0]['steps']:
        start_location = step['start_location']
        end_location = step['end_location']
        
        route_coordinates.append((start_location['lat'], start_location['lng']))
        route_coordinates.append((end_location['lat'], end_location['lng']))
    
    return route_coordinates

def get_route(start: PubData, end: PubData, gmaps: googlemaps.Client, routes_cache: set) -> tuple:
    directions = gmaps.directions(
        origin=(start.latitude, start.longitude),
        destination=(end.latitude, end.longitude),
        mode="walking", 
        departure_time=datetime.datetime.now()
    )
    
    if not directions:
        return None

    route = directions[0]
    distance = route['legs'][0]['distance']['text']
    duration = route['legs'][0]['duration']['text']
        
    # Get the coordinates using the helper function
    route_coordinates = get_route_coordinates(route)
    
    return (start.name, end.name, {"duration": convert_duration_to_minutes(duration), "distance": distance, "route_coordinates": route_coordinates})

def convert_duration_to_minutes(duration_str: str) -> int:
    time_match = re.match(r"(\d+)\s*(min|mins|minute|minutes|hour|hours|h)", duration_str.lower())
    if time_match:
        quantity = int(time_match.group(1))
        unit = time_match.group(2)
        return quantity if unit in ["min", "mins", "minute", "minutes"] else quantity * 60
    return 0


def fetch_pub_routes(pubs: list[PubData]) -> list[tuple]:
    routes_cache = set()
    routes = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_route = {}
        for pub in pubs:
            nearest_pubs = get_nearest_pubs(pub, pubs)
            for nearest_pub in nearest_pubs:
                future = executor.submit(get_route, pub, nearest_pub, gmaps, routes_cache)
                future_to_route[future] = (pub, nearest_pub)
        
        for future in future_to_route:
            result = future.result()
            if result:
                routes.append(result)

    return routes


def create_graph_from_routes(routes: list[tuple[str, str, str, str]], pubs: list[PubData]) -> UndirectedGraph:
    g = UndirectedGraph()
    pub_map = {pub.name: Location(pub.latitude, pub.longitude, pub.name, 
                                  attr = {"address": pub.address, "source": pub.source, "distance_km": pub.distance_km,
                                          "place_id": pub.place_id, "rating":pub.rating, "user_ratings_total": pub.user_ratings_total,
                                          "phone_number": pub.phone_number, "photo_reference": pub.photo_reference}) for pub in pubs}

    for pub in pubs:
        g.add_location(pub_map[pub.name])

    for start_name, end_name, args in routes:
        start_pub = pub_map.get(start_name)
        end_pub = pub_map.get(end_name)
        if start_pub and end_pub:
            g.add_edge(start_pub, end_pub, args["duration"])

    return g, pub_map


def add_shortest_edges_to_connect_graph(graph: UndirectedGraph, pubs: list[Location], pub_map) -> UndirectedGraph:
    # Simple approach to ensure the graph is connected:
    # If there are disconnected components, add edges between them.
    
    connected_pubs = set()
    
    def dfs(pub, visited):
        visited.add(pub.name)
        connected_pubs.add(pub.name)
        for neighbor in graph.get_neighbors(pub):
            if neighbor[0].name not in visited:
                dfs(neighbor[0], visited)
    
    # Start DFS from the first pub to mark all reachable pubs
    visited = set()
    starting_vertex = graph.vertices()[0]
    print(graph.adjacency_list)

    dfs(starting_vertex, visited)
    
    # If not all pubs are visited, add the shortest edges between unconnected pubs
    for pub in pubs:
        if pub.name not in connected_pubs:
            # Find the nearest connected pub
            nearest_pub = min(connected_pubs, key=lambda connected_pub: geodesic(
                (pub.latitude, pub.longitude), 
                (next(p for p in pubs if p.name == connected_pub).latitude, 
                 next(p for p in pubs if p.name == connected_pub).longitude)).km)

            # Add the shortest edge
            new_route = get_route(pub_map[nearest_pub], pub_map[pub.name], gmaps, set())
            graph.add_edge(pub_map[nearest_pub], pub_map[pub.name], new_route[3])

    return graph


def convert_route_to_json(routes: list[tuple[str, str, str, str]], pubs: list[Pub]) -> list[Route]:
    best_routes = []

    for start_name, end_name, args in routes:
        start_pub = next(pub for pub in pubs if pub.name == start_name)
        end_pub = next(pub for pub in pubs if pub.name == end_name)
        
        time = args["duration"]
        distance = int(args["distance"].split()[0])
        
        route = Route(
            start_node=start_pub,
            end_node=end_pub,
            time=time,
            distance=distance,
            route=args["route_coordinates"]
        )
        
        best_routes.append(route)

    best_routes.sort(key=lambda r: (r.time, r.distance))

    return json.dumps(best_routes)

def get_best_route(routes_by_pub):
    best_node_w = -math.inf
    worst_node_w = math.inf
    best_node = None
    worst_node = None

    for _r, w in routes_by_pub:
        if w > best_node_w:
            best_node_w = w
            best_node = _r
        if w < worst_node_w:
            worst_node_w = w
            worst_node = _r
    
    print("\n\nBest Route")
    print("WEIGHT = " + str(best_node_w) + "   ::   ", end="")
    print(best_node)
    best_nodes = []

    for n in best_node:
        best_nodes.append(Pub(n.name, (n.latitude, n.longitude), n.attr["rating"]))
        print("\t> " + str(n), end="\n")
    
    # get the routes corresponding to this path
    # return a list of
    

def process_pubs(latitude: float, longitude: float, radius_km: float):
    pubs = get_pubs(API_KEY, latitude, longitude, radius_km)
    pubs = normalize_pub_ratings(pubs)
    routes = fetch_pub_routes(pubs)
    
    graph, pub_map = create_graph_from_routes(routes, pubs)
    graph = add_shortest_edges_to_connect_graph(graph, pubs, pub_map)

    routes_by_pub = get_all_routes(graph, MAX_PUBS)

    best_route = get_best_route(routes_by_pub)

    visualize_graph(graph)


if __name__ == "__main__":
    latitude, longitude = 52.953250, -1.150500
    radius_km = 3
    process_pubs(latitude, longitude, radius_km)
