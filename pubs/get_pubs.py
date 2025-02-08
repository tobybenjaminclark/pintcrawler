import googlemaps
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
    rating: float = 0  # Default to 0 if no rating is available
    user_ratings_total: int = 0  # Total number of ratings
    phone_number: str = "Unknown Phone Number"
    website: str = "Unknown Website"
    price_level: int = -1  # Price level (0-4)
    photo_reference: str = ""  # Photo reference for fetching photos

    def __str__(self):
        return (f"Pub: {self.name}\n"
                f"Source: {self.source}\n"
                f"Address: {self.address}\n"
                f"Location: ({self.latitude}, {self.longitude})\n"
                f"Distance: {self.distance_km} km\n"
                f"Rating: {self.rating}\n"
                f"Photo Reference: {self.photo_reference if self.photo_reference else 'No Photos'}\n")

def get_pubs(api_key: str, latitude: float, longitude: float, radius_meters: int) -> list[PubData]:
    """
    Fetches pubs from Google Places API within a given radius and includes detailed information.
    """
    gmaps = googlemaps.Client(key=api_key)
    
    places = gmaps.places_nearby(
        location=(latitude, longitude),
        radius=radius_meters,
        type="pub"
    )
    
    pubs = []
    for place in places.get("results", []):
        pub_name = place.get("name", "Unknown Pub")
        lat = place["geometry"]["location"]["lat"]
        lon = place["geometry"]["location"]["lng"]
        address = place.get("vicinity", "Unknown Address")
        place_id = place.get("place_id", "")
        rating = place.get("rating", -1.0)
        
        # Optionally, check for photos (only first photo reference for now)
        photo_reference = ""
        if "photos" in place:
            photo_reference = place["photos"][0].get("photo_reference", "")
        
        distance = geodesic((latitude, longitude), (lat, lon)).km
        pubs.append(PubData(
            name=pub_name,
            latitude=lat,
            longitude=lon,
            address=address,
            source="Google",
            distance_km=round(distance, 2),
            rating=rating,
            place_id=place_id,
            photo_reference=photo_reference
        ))
    
    return pubs


if __name__ == "__main__":
    latitude, longitude = 51.5074, -0.1278  # London
    radius_meters = 2000  # 2km

    pubs = get_pubs(API_KEY, latitude, longitude, radius_meters)

    for pub in pubs:
        print(pub)
