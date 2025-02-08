import datetime
import googlemaps
from geopy.distance import geodesic
from concurrent.futures import ThreadPoolExecutor
from get_pubs import PubData, get_pubs
from api_key import API_KEY
from graph import UndirectedGraph
from location import Location
from visualise import visualize_graph
from router import get_all_routes
import re

gmaps = googlemaps.Client(key=API_KEY)


def get_nearest_pubs(pub: PubData, pubs: list[PubData], n: int = 3) -> list[PubData]:
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
            
            new_route = get_route(pub_map[nearest_pub], pub_map[pub.name], gmaps, set())
            # Add the shortest edge
            graph.add_edge(pub_map[nearest_pub], pub_map[pub.name], new_route[3])

    return graph



if __name__ == "__main__":
    latitude, longitude = 52.947957, -1.182484

    radius_km = 1

    pubs = get_pubs(API_KEY, latitude, longitude, radius_km)

    
    for pub in pubs:
        print(f"pub: {pub.name}\n lat: {pub.latitude}\n long:{pub.longitude}\n \n\n")
    routes = fetch_pub_routes(pubs)
    for route in routes:
        print(route)

    graph, pub_map = create_graph_from_routes(routes, pubs)
    
    # Add shortest routes to connect disconnected components
    graph = add_shortest_edges_to_connect_graph(graph, pubs, pub_map)

    """# Get all routes starting from each pub
    routes_by_pub = get_all_routes(graph)

    # Print out the routes for each starting pub
    for start_pub, routes in routes_by_pub.items():
        print(f"Routes starting from {start_pub}:")
        for route in routes:
            for n in route:
                s_n = str(n)
                print(" > " + s_n , end = "")
            print("")"""
 
    visualize_graph(graph)

