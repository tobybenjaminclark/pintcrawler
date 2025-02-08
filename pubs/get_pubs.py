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
    source: str = "Google"
    distance_km: float = 0.0
    place_id: str = ""
    rating: float = 0  
    user_ratings_total: int = 0 
    phone_number: str = "Unknown Phone Number"
    website: str = "Unknown Website"
    photo_reference: str = "" 

    def __str__(self):
        return (f"Pub: {self.name}\n"
                f"Source: {self.source}\n"
                f"Address: {self.address}\n"
                f"Location: ({self.latitude}, {self.longitude})\n"
                f"Distance: {self.distance_km} km\n"
                f"Rating: {self.rating} ({self.user_ratings_total} ratings)\n"
                f"Phone: {self.phone_number}\n"
                f"Website: {self.website}\n"
                f"Photo Reference: {self.photo_reference if self.photo_reference else 'No Photos'}\n")

def get_pubs(api_key: str, latitude: float, longitude: float, radius_km: int) -> list[PubData]:
    """
    Fetches pubs from Google Places API using a search query and includes detailed information 
    from Contact and Atmosphere categories within a given radius.
    """
    gmaps = googlemaps.Client(key=api_key)
    
    places = gmaps.places(
        location=(latitude, longitude),
        query="pub"
    )
    
    pubs = []
    for place in places.get("results", []):
        pub_name = place.get("name", "Unknown Pub")
        lat, lon = place["geometry"]["location"].values()
        address = place.get("vicinity", "Unknown Address")
        place_id = place.get("place_id", "")
        
        # Fetch detailed information for each pub
        place_details = gmaps.place(
            place_id=place_id,
            fields=["formatted_address", "formatted_phone_number", "international_phone_number", "opening_hours", 
                    "website", "rating", "user_ratings_total", "photo", "serves_beer", 
                    "serves_breakfast", "serves_brunch", "serves_dinner", "serves_lunch", "serves_vegetarian_food"]
        )
        
        details = place_details.get("result", {})
        rating = details.get("rating", 0.0)
        user_ratings_total = details.get("user_ratings_total", 0)
        phone_number = details.get("formatted_phone_number", "Unknown Phone Number")
        website = details.get("website", "Unknown Website")

        # Optionally, check for photos (only first photo reference for now)
        photo_reference = details.get("photos", [{}])[0].get("photo_reference", "")
        
        # Calculate distance
        distance = geodesic((latitude, longitude), (lat, lon)).km
        pubs.append(PubData(
            name=pub_name,
            latitude=lat,
            longitude=lon,
            address=address,
            source="Google",
            distance_km=round(distance, 2),
            rating=rating,
            user_ratings_total=user_ratings_total,
            phone_number=phone_number,
            website=website,
            photo_reference=photo_reference
        ))
    
    pubs = filter_pubs_within_radius(pubs, latitude, longitude, radius_km)
    return pubs

def filter_pubs_within_radius(pubs: list, latitude: float, longitude: float, search_radius_km: float) -> list:
    """
    Filters out pubs that are further than the specified search radius.
    """
    filtered_pubs = []
    
    for pub in pubs:
        distance = geodesic((latitude, longitude), (pub.latitude, pub.longitude)).km
        if distance <= search_radius_km:
            filtered_pubs.append(pub)
    
    return filtered_pubs

if __name__ == "__main__":
    latitude, longitude = 52.953340, -1.149964
    radius_meters = 2000  # 2km

    pubs = get_pubs(API_KEY, latitude, longitude, radius_meters)

    for pub in pubs:
        print(pub)
