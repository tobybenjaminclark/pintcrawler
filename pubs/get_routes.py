# get_routes.py

import datetime
from dataclasses import is_dataclass, asdict

import googlemaps
import re
import math
from geopy.distance import geodesic
from concurrent.futures import ThreadPoolExecutor
from get_pubs import PubData, get_pubs, normalize_pub_ratings
from api_key import API_KEY
from graph import UndirectedGraph
from location import Location
from visualise import visualize_graph
from router import get_all_routes
from route import Route, Pub  # Import your dataclasses for route segments
import polyline  # used to decode encoded polylines
import json

gmaps = googlemaps.Client(key=API_KEY)

MAX_PUBS = 4


def get_nearest_pubs(pub: PubData, pubs: list[PubData], n: int = 3) -> list[PubData]:
    distances = [
        (geodesic((pub.latitude, pub.longitude), (other_pub.latitude, other_pub.longitude)).km, other_pub)
        for other_pub in pubs if other_pub != pub
    ]
    distances.sort(key=lambda x: x[0])
    return [other_pub for _, other_pub in distances[:n]]


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
    return (start.name, end.name, distance, convert_duration_to_minutes(duration))


def convert_duration_to_minutes(duration_str: str) -> int:
    time_match = re.match(r"(\d+)\s*(min|mins|minute|minutes|hour|hours|h)", duration_str.lower())
    if time_match:
        quantity = int(time_match.group(1))
        unit = time_match.group(2)
        return quantity if unit in ["min", "mins", "minute", "minutes"] else quantity * 60
    return 0


def get_route_with_polyline(start: Location, end: Location, gmaps: googlemaps.Client):
    """
    For a given pair of Location objects, request directions (walking)
    and extract the distance (meters), duration (minutes) and decode the
    overview polyline into a list of (latitude, longitude) points.
    """
    directions = gmaps.directions(
        origin=(start.latitude, start.longitude),
        destination=(end.latitude, end.longitude),
        mode="walking",
        departure_time=datetime.datetime.now()
    )
    if not directions:
        return None
    route_info = directions[0]
    leg = route_info['legs'][0]
    distance = leg['distance']['value']  # distance in meters
    duration_seconds = leg['duration']['value']
    duration_minutes = duration_seconds // 60
    polyline_str = route_info.get('overview_polyline', {}).get('points', '')
    points = polyline.decode(polyline_str) if polyline_str else []
    return distance, duration_minutes, points


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


def create_graph_from_routes(routes: list[tuple[str, str, str, str]], pubs: list[PubData]) -> tuple[UndirectedGraph, dict]:
    g = UndirectedGraph()
    pub_map = {
        pub.name: Location(
            pub.latitude,
            pub.longitude,
            pub.name,
            attr={
                "address": pub.address,
                "source": pub.source,
                "distance_km": pub.distance_km,
                "place_id": pub.place_id,
                "rating": pub.rating,
                "user_ratings_total": pub.user_ratings_total,
                "phone_number": pub.phone_number,
                "photo_reference": pub.photo_reference
            }
        )
        for pub in pubs
    }
    for pub in pubs:
        g.add_location(pub_map[pub.name])
    for start_name, end_name, distance, time in routes:
        start_pub = pub_map.get(start_name)
        end_pub = pub_map.get(end_name)
        if start_pub and end_pub:
            g.add_edge(start_pub, end_pub, time)
    return g, pub_map


def add_shortest_edges_to_connect_graph(graph: UndirectedGraph, pubs: list[Location], pub_map) -> UndirectedGraph:
    # Simple approach to ensure the graph is connected:
    connected_pubs = set()

    def dfs(pub, visited):
        visited.add(pub.name)
        connected_pubs.add(pub.name)
        for neighbor in graph.get_neighbors(pub):
            if neighbor[0].name not in visited:
                dfs(neighbor[0], visited)

    visited = set()
    print(graph.vertices())
    starting_vertex = graph.vertices()[0]
    dfs(starting_vertex, visited)
    for pub in pubs:
        if pub.name not in connected_pubs:
            # Find the nearest connected pub
            nearest_pub = min(
                connected_pubs,
                key=lambda connected_pub: geodesic(
                    (pub.latitude, pub.longitude),
                    (next(p for p in pubs if p.name == connected_pub).latitude,
                     next(p for p in pubs if p.name == connected_pub).longitude)
                ).km
            )
            new_route = get_route(pub_map[nearest_pub], pub_map[pub.name], gmaps, set())
            if new_route:
                graph.add_edge(pub_map[nearest_pub], pub_map[pub.name], new_route[3])
    return graph


def main_router(lat, long) -> list[Route]:
    """
    Main routine: fetch pubs, build the route graph, select the best route,
    and then for each consecutive pair of pubs in the best route, call the directions API
    to retrieve (and decode) the polyline. For each segment a Route object is created.
    The function returns the list of Route objects for the best route.
    """
    # Get pubs and build graph
    longitude, latitude  = lat, long
    radius_km = 8
    print(latitude,longitude)
    pubs = get_pubs(API_KEY, latitude, longitude, radius_km)
    pubs = normalize_pub_ratings(pubs)
    print(pubs)
    routes = fetch_pub_routes(pubs)
    print(routes)
    graph, pub_map = create_graph_from_routes(routes, pubs)
    print(graph, pub_map)
    graph = add_shortest_edges_to_connect_graph(graph, pubs, pub_map)

    # Get all routes from the graph (each route is a list of vertices with a weight)
    routes_by_pub = get_all_routes(graph)
    gl_routes = []
    for start_pub, routes_list in routes_by_pub.items():
        for route, w in routes_list:
            gl_routes.append((route, w))
    gl_routes = list(filter(lambda route: len(route[0]) < MAX_PUBS, gl_routes))

    # Select best (and worst) route by weight
    best_node_w = -math.inf
    worst_node_w = math.inf
    best_node = None
    worst_node = None
    for _r, w in gl_routes:
        if w > best_node_w:
            best_node_w = w
            best_node = _r
        if w < worst_node_w:
            worst_node_w = w
            worst_node = _r

    print("\n\nBest Route")
    print("WEIGHT = " + str(best_node_w) + "   ::   ", end="")
    print(best_node)
    for n in best_node:
        print(" > " + str(n), end="")
    print("\n\nWorst Route")
    print("WEIGHT = " + str(worst_node_w) + "   ::   ", end="")
    print(worst_node)
    for n in worst_node:
        print(" > " + str(n), end="")
    print("\n")

    # Now build the list of Route objects for the best route.
    best_route_segments = []
    if best_node and len(best_node) >= 2:
        for i in range(len(best_node) - 1):
            segment_info = get_route_with_polyline(best_node[i], best_node[i + 1], gmaps)
            if segment_info is not None:
                distance, time_minutes, points = segment_info
                # Convert the Location object to a route.Pub object.
                start_pub = Pub(
                    name=best_node[i].name,
                    loc=(best_node[i].latitude, best_node[i].longitude),
                    rating=best_node[i].attr.get("rating", 0)
                )
                end_pub = Pub(
                    name=best_node[i + 1].name,
                    loc=(best_node[i + 1].latitude, best_node[i + 1].longitude),
                    rating=best_node[i + 1].attr.get("rating", 0)
                )
                best_route_segments.append(Route(
                    start_node=start_pub,
                    end_node=end_pub,
                    time=time_minutes,
                    distance=distance,
                    route=points
                ))

    # Optionally, visualize the graph.
    #visualize_graph(graph)

    return best_route_segments

def dataclass_to_json(obj: any) -> str:
    """
    Convert a dataclass instance (or a list of dataclass instances)
    to a JSON string.
    """
    def convert(item):
        if is_dataclass(item):
            return asdict(item)
        elif isinstance(item, (list, tuple)):
            return [convert(i) for i in item]
        else:
            return item

    # Handle both a single dataclass or a list of them.
    converted_obj = convert(obj)
    return json.dumps(converted_obj, indent=2)


if __name__ == "__main__":
    best_segments = main_router(51.426099, -0.566008)
    print("Best route segments (with polyline coordinates):")
    for segment in best_segments:
        print(segment)
    routes_json = dataclass_to_json(best_segments)
    print(routes_json)