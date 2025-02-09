import requests
import folium
from folium.plugins import MarkerCluster

def get_crimes_by_point(lat, lng, date="2024-01", category="all-crime"):
    """
    Fetch street-level crimes around a specific point.

    Args:
        lat (float or str): Latitude of the location.
        lng (float or str): Longitude of the location.
        date (str): Month of interest in 'YYYY-MM' format. Default is "2024-01".
        category (str): The crime category to query. Default is "all-crime".

    Returns:
        list: A list of crime records (each as a dictionary), or None if an error occurs.
    """
    url = f"https://data.police.uk/api/crimes-street/{category}"
    params = {
        "date": date,
        "lat": lat,
        "lng": lng
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        crimes = response.json()
        return crimes
    except requests.RequestException as e:
        print(f"Error fetching crimes by point: {e}")
        return None

def plot_crimes(crimes, lat, lng):
    """
    Plot crimes on an interactive map using Folium.

    Args:
        crimes (list): List of crime records fetched from the API.
        lat (float): Latitude of the central point.
        lng (float): Longitude of the central point.
    """
    # Create a map centered on the given coordinates
    crime_map = folium.Map(location=[lat, lng], zoom_start=14, control_scale=True)

    # Add marker cluster for better visualization of crime points
    marker_cluster = MarkerCluster().add_to(crime_map)

    # Plot the central point (user's location)
    folium.Marker(
        location=[lat, lng],
        popup="Start Location",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(crime_map)

    # Plot the crime points on the map
    for crime in crimes:
        crime_lat = float(crime['location']['latitude'])
        crime_lng = float(crime['location']['longitude'])
        
        folium.Marker(
            location=[crime_lat, crime_lng],
            popup=f"Crime: {crime['category']}",
            icon=folium.Icon(color="red", icon="cloud")
        ).add_to(marker_cluster)

    # Display the map
    crime_map.save("crime_map.html")

if __name__ == '__main__':
    # Example 1: Specific point query
    lat, lng = 51.569232, 0.451880  # Example coordinates
    crimes_point = get_crimes_by_point(lat, lng, date="2024-01")

    if crimes_point is not None:
        print(f"Crimes near the point ({lat}, {lng}):")
        for crime in crimes_point:
            print(crime)
        
        # Plot the crimes on the map
        plot_crimes(crimes_point, lat, lng)
        print("Map saved as 'crime_map.html'. Open this file in your browser to view the map.")
    else:
        print("No data for the specific point query.")
