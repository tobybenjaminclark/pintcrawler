from graph import UndirectedGraph
from location import Location
from visualise import visualize_graph

def example_usage():
    # Create a new graph
    g = UndirectedGraph()

    # Create 14 pubs (using fictional or approximate coordinates)
    # (Lat, Lon, unique_id, additional_info)
    pub1 = Location(51.5014, -0.1419, "PUB_1", {"city": "London", "name": "The Red Lion"})
    pub2 = Location(51.5033, -0.1195, "PUB_2", {"city": "London", "name": "The King's Arms"})
    pub3 = Location(51.5094, -0.1182, "PUB_3", {"city": "London", "name": "The Crown"})
    pub4 = Location(51.5115, -0.1163, "PUB_4", {"city": "London", "name": "The King's Head"})
    pub5 = Location(51.5145, -0.1202, "PUB_5", {"city": "London", "name": "Old Tavern"})
    pub6 = Location(51.5167, -0.1300, "PUB_6", {"city": "London", "name": "The Fox & Anchor"})
    pub7 = Location(51.5180, -0.1357, "PUB_7", {"city": "London", "name": "The Golden Fleece"})
    pub8 = Location(51.5195, -0.1412, "PUB_8", {"city": "London", "name": "The Dog & Duck"})
    pub9 = Location(51.5210, -0.1438, "PUB_9", {"city": "London", "name": "The Merry Monk"})
    pub10 = Location(51.5230, -0.1462, "PUB_10", {"city": "London", "name": "Ye Olde Ale House"})
    pub11 = Location(51.5245, -0.1490, "PUB_11", {"city": "London", "name": "The Drunken Sailor"})
    pub12 = Location(51.5255, -0.1520, "PUB_12", {"city": "London", "name": "The Rose & Crown"})
    pub13 = Location(51.5267, -0.1575, "PUB_13", {"city": "London", "name": "The Lion & Unicorn"})
    pub14 = Location(51.5280, -0.1602, "PUB_14", {"city": "London", "name": "The Old Barrel"})

    pubs = [
        pub1, pub2, pub3, pub4, pub5, pub6, pub7,
        pub8, pub9, pub10, pub11, pub12, pub13, pub14
    ]

    # Add them to the graph
    for p in pubs:
        g.add_location(p)

    # Connect them in a snake/chain (pub1->pub2->pub3->...->pub14)
    # with fictional distances (you can replace with real or computed ones)
    chain_edges = [
        (pub1, pub2, 1.2),
        (pub2, pub3, 0.8),
        (pub3, pub4, 0.6),
        (pub4, pub5, 1.0),
        (pub5, pub6, 1.1),
        (pub6, pub7, 0.9),
        (pub7, pub8, 0.5),
        (pub8, pub9, 0.7),
        (pub9, pub10, 1.3),
        (pub10, pub11, 0.6),
        (pub11, pub12, 0.7),
        (pub12, pub13, 1.4),
        (pub13, pub14, 0.9)
    ]
    for (src, dst, dist) in chain_edges:
        g.add_edge(src, dst, weight=dist)

    # Add a few extra edges for partial connectivity (not a full mesh, just some shortcuts)
    # These can be arbitrary connections you want to spice up the graph
    extra_edges = [
        (pub2, pub5, 2.5),
        (pub4, pub7, 2.0),
        (pub8, pub12, 1.8)
    ]
    for (src, dst, dist) in extra_edges:
        g.add_edge(src, dst, weight=dist)

    # Print some info to verify
    print("Vertices:", g.vertices())
    print("Edges:", g.edges())

    # Visualize
    visualize_graph(g)

if __name__ == "__main__":
    example_usage()
