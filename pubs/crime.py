import requests

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


if __name__ == '__main__':
    # Example 1: Specific point query
    lat, lng = 51.569232, 0.451880
    crimes_point = get_crimes_by_point(lat, lng, date="2024-01")
    if crimes_point is not None:
        print("Crimes near the point:")
        for crime in crimes_point:
            print(crime)
    else:
        print("No data for the specific point query.")


