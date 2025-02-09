from flask import Flask, request, jsonify
from get_routes import main_router
from flask_cors import CORS

app = Flask(__name__)

@app.route('/', methods=['OPTIONS'])
def hello_http():
    """
    Endpoint that mimics the behavior of your Cloud Function.
    Expects a JSON payload with "lat" and "long" keys.
    """
    print("testinggg")
    request_json = request.get_json(silent=True)
    print("testingggfdasfsaf")
    if request_json and "lat" in request_json and "long" in request_json:
        print("test")
        # Call your main_router function with the provided latitude and longitude.
        result = main_router(request_json["lat"], request_json["long"])
        return jsonify(result)
    else:
        print("test1")
        # Return an error response if required parameters are missing.
        return jsonify({"error": 100}), 400
CORS(app, 
     resources={r"/*": {"origins": "*"}},
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Origin"])
if __name__ == '__main__':
    # Run the server in debug mode on host 0.0.0.0 and port 5000.
    app.run(debug=True, host='0.0.0.0', port=5069)
