from dataclasses import dataclass

@dataclass
class Pub:
    name: str
    loc: [float, float]
    rating: int # 1 to 5

@dataclass
class Route:
    start_node: Pub
    end_node: Pub
    time: int # minutes
    distance: int # yards
    route: list[tuple[float, float]]

# [Route]