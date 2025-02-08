from dataclasses import dataclass
from graph import UndirectedGraph
from location import Location

@dataclass
class RoutingParameters:
    w_rating: float
    w_walking: float

def get_route(g: UndirectedGraph, p: RoutingParameters) -> [Location]:
    return []