from dataclasses import dataclass

@dataclass
class Location():
    lat: float
    long: float
    name: str
    attr: dict

    def __repr__(self) -> str:
        return self.name

    def __eq__(self, other):
        if not isinstance(other, Location):
            return False
        return (self.lat, self.long) == (other.lat, other.long)

    def __hash__(self):
        # You must return an integer that is stable for the object's lifetime
        return hash((self.lat, self.long))

    def get_weight(self) -> float:
        return 5