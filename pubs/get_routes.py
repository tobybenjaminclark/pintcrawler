import datetime
import googlemaps
from geopy.distance import geodesic
from concurrent.futures import ThreadPoolExecutor
from get_pubs import PubData, get_pubs
from api_key import API_KEY
from graph import UndirectedGraph
from location import Location
from visualise import visualize_graph
import re


def get_nearest_pubs(pub: PubData, pubs: list[PubData], n: int = 3) -> list[PubData]:
    distances = [(geodesic((pub.latitude, pub.longitude), (other_pub.latitude, other_pub.longitude)).km, other_pub)
                 for other_pub in pubs if other_pub != pub]
    distances.sort(key=lambda x: x[0])
    return [other_pub for _, other_pub in distances[:n]]


def get_route(start: PubData, end: PubData, gmaps: googlemaps.Client, routes_cache: set) -> tuple:
    route_key = (start.place_id, end.place_id)
    reverse_route_key = (end.place_id, start.place_id)
    
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

    routes_cache.add(route_key)
    routes_cache.add(reverse_route_key)

    return (start.name, end.name, distance, convert_duration_to_minutes(duration))


def convert_duration_to_minutes(duration_str: str) -> int:
    time_match = re.match(r"(\d+)\s*(min|mins|minute|minutes|hour|hours|h)", duration_str.lower())
    if time_match:
        quantity = int(time_match.group(1))
        unit = time_match.group(2)
        return quantity if unit in ["min", "mins", "minute", "minutes"] else quantity * 60
    return 0


def fetch_pub_routes(api_key: str, pubs: list[PubData]) -> list[tuple]:
    gmaps = googlemaps.Client(key=api_key)
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
    pub_map = {pub.name: Location(pub.latitude, pub.longitude, pub.place_id, {"name": pub.name}) for pub in pubs}

    for pub in pubs:
        g.add_location(pub_map[pub.name])

    for start_name, end_name, distance, time in routes:
        start_pub = pub_map.get(start_name)
        end_pub = pub_map.get(end_name)
        if start_pub and end_pub:
            g.add_edge(start_pub, end_pub, time)

    return g


if __name__ == "__main__":
    latitude, longitude = 52.9540, 1.1550
    radius_meters = 2000 

    pubs = get_pubs(API_KEY, latitude, longitude, radius_meters)
    routes = fetch_pub_routes(API_KEY, pubs)

    graph = create_graph_from_routes(routes, pubs)
    
    print("Vertices:", graph.vertices())
    print("Edges:", graph.edges())
    
    visualize_graph(graph)
