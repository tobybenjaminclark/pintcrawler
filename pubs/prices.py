import requests
import folium
from folium.plugins import MarkerCluster

def get_pub_prices_by_point(lat, lng, radius=500):
    """
    Fetch pub prices around a specific point.

    Args:
        lat (float or str): Latitude of the location.
        lng (float or str): Longitude of the location.
        radius (int): Search radius in meters. Default is 500m.

    Returns:
        list: A list of pub price records (each as a dictionary), or None if an error occurs.
    """
    url = "https://api.pubprices.com/v1/pubs"
    params = {
        "lat": lat,
        "lng": lng,
        "radius": radius
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        pubs = response.json()
        return pubs
    except requests.RequestException as e:
        print(f"Error fetching pub prices by point: {e}")
        return None

def plot_pub_prices(pubs, lat, lng):
    """
    Plot pub prices on an interactive map using Folium.

    Args:
        pubs (list): List of pub records fetched from the API.
        lat (float): Latitude of the central point.
        lng (float): Longitude of the central point.
    """
    pub_map = folium.Map(location=[lat, lng], zoom_start=14, control_scale=True)
    marker_cluster = MarkerCluster().add_to(pub_map)

    folium.Marker(
        location=[lat, lng],
        popup="Start Location",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(pub_map)

    for pub in pubs:
        pub_lat = float(pub['latitude'])
        pub_lng = float(pub['longitude'])
        pub_name = pub['name']
        pub_price = pub.get('average_price', 'Unknown')

        folium.Marker(
            location=[pub_lat, pub_lng],
            popup=f"{pub_name}: £{pub_price}",
            icon=folium.Icon(color="green", icon="glass")
        ).add_to(marker_cluster)

    pub_map.save("pub_map.html")

if __name__ == '__main__':
    lat, lng = 51.5074, -0.1278  # Example: London coordinates
    pubs = get_pub_prices_by_point(lat, lng, radius=1000)
    
    if pubs is not None:
        print(f"Pubs near ({lat}, {lng}):")
        for pub in pubs:
            print(pub)
        
        plot_pub_prices(pubs, lat, lng)
        print("Map saved as 'pub_map.html'. Open this file in your browser to view the map.")
    else:
        print("No pub data found.")
