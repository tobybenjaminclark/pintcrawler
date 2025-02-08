import googlemaps
import overpy
from geopy.distance import geodesic
from dataclasses import dataclass
from api_key import API_KEY


@dataclass
class PubData:
    name: str
    latitude: float
    longitude: float
    address: str = "Unknown Address"
    source: str = "Unknown Source"
    distance_km: float = 0.0
    place_id: str = ""  

def get_pubs_from_google(api_key: str, latitude: float, longitude: float, radius_meters: int) -> list[PubData]:
    """
    Fetches pubs from Google Places API within a given radius.
    """
    gmaps = googlemaps.Client(key=api_key)
    
    places = gmaps.places_nearby(
        location=(latitude, longitude),
        radius=radius_meters,
        type="bar"  # Google Maps doesn't have "pub", but "bar" includes pubs
    )
    
    pubs = []
    for place in places.get("results", []):
        pub_name = place.get("name", "Unknown Pub")
        lat = place["geometry"]["location"]["lat"]
        lon = place["geometry"]["location"]["lng"]
        address = place.get("vicinity", "Unknown Address")
        place_id = place.get("place_id", "")
        
        distance = geodesic((latitude, longitude), (lat, lon)).km
        pubs.append(PubData(name=pub_name, latitude=lat, longitude=lon, address=address, source="Google", distance_km=round(distance, 2), place_id=place_id))
    
    return pubs

def get_pubs_from_osm(latitude: float, longitude: float, radius_meters: int) -> list[PubData]:
    """
    Fetches pubs from OpenStreetMap's Overpass API within a given radius.
    """
    api = overpy.Overpass()
    query = f"""
    [out:json];
    node["amenity"="pub"](around:{radius_meters},{latitude},{longitude});
    out;
    """
    
    result = api.query(query)
    
    pubs = []
    for node in result.nodes:
        pub_location = (float(node.lat), float(node.lon))
        distance = geodesic((latitude, longitude), pub_location).km
        pub_name = node.tags.get("name", "Unknown Pub")
        
        pubs.append(PubData(name=pub_name, latitude=node.lat, longitude=node.lon, source="OSM", distance_km=round(distance, 2)))
    
    return pubs

def get_pubs(api_key: str, latitude: float, longitude: float, radius_meters: int) -> list[PubData]:
    """
    Combines Google Places and OpenStreetMap pub data.
    """
    google_pubs = get_pubs_from_google(api_key, latitude, longitude, radius_meters)
    osm_pubs = get_pubs_from_osm(latitude, longitude, radius_meters)
    
    # Merge lists (no deduplication yet)
    all_pubs = google_pubs + osm_pubs
    
    return all_pubs

if __name__ == "__main__":
    latitude, longitude = 51.5074, -0.1278  # London
    radius_meters = 2000  # 2km

    pubs = get_pubs(API_KEY, latitude, longitude, radius_meters)

    for pub in pubs:
        print(f"Source: {pub.source} | Pub: {pub.name} | Location: ({pub.latitude}, {pub.longitude}) | Distance: {pub.distance_km} km | Address: {pub.address}")
