from dataclasses import dataclass

@dataclass
class Location():
    latitude: float
    longitude: float
    name: str    
    attr: dict
    """address: str = "Unknown Address"
    source: str = "Google"
    distance_km: float = 0.0
    place_id: str = ""
    rating: float = 0  
    user_ratings_total: int = 0 
    phone_number: str = "Unknown Phone Number"
    website: str = "Unknown Website"
    photo_reference: str = "" """

    def __repr__(self) -> str:
        return self.name + " (" + str(self.attr["rating"]) + ")"

    def __eq__(self, other):
        if not isinstance(other, Location):
            return False
        return (self.latitude, self.longitude) == (other.latitude, other.longitude)

    def __hash__(self):
        # You must return an integer that is stable for the object's lifetime
        return hash((self.latitude, self.longitude))

    def get_weight(self) -> float:
        return 5