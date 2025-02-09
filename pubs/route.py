from dataclasses import dataclass

@dataclass
class Pub:
    name: str
    loc: tuple[float, float]
    rating: int

@dataclass
class Route:
    start_node: Pub
    end_node: Pub
    time: int
    distance: int 
    route: list[tuple[float, float]]
