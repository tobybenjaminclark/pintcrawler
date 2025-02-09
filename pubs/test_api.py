import requests

url = "https://get-route-863661396582.europe-north1.run.app/get-route"
payload = {"lat": 51.573128, "long": 0.481039}

response = requests.post(url, json=payload)

# Print the raw text of the response
print(response.text)

# If you expect a JSON response, you can parse it like this:
try:
    data = response.json()
    print(data)
except ValueError:
    print("Response is not in JSON format.")
