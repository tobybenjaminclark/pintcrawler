import requests

url = "https://europe-north1-evrp2-426411.cloudfunctions.net/get-route"
payload = {"lat": 55, "long": 52}

response = requests.post(url, json=payload)

# Print the raw text of the response
print(response.text)

# If you expect a JSON response, you can parse it like this:
try:
    data = response.json()
    print(data)
except ValueError:
    print("Response is not in JSON format.")
