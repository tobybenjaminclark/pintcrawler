from flask import Flask, request, jsonify
from get_routes import main_router
from flask_cors import CORS

app = Flask(__name__)

@app.route('/', methods=['POST'])
def hello_http():
    """
    Endpoint that mimics the behavior of your Cloud Function.
    Expects a JSON payload with "lat" and "long" keys.
    """
    print("testinggg")
    request_json = request.get_json(silent=True)

    required_params = [
        "lat",
        "long",
        "maximise_rating",
        "range",
        "walking",
        "warrior_mode"
    ]

    missing = False
    for param in required_params:
        if param not in request_json:
            print(f"{param} missing from JSON")
            missing = True
        if missing:
            return jsonify({"error": 100}), 400

    result = main_router(request_json["lat"], request_json["long"], request_json)
    return jsonify(result)

CORS(app, 
     resources={r"/*": {"origins": "*"}},
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Origin"])
if __name__ == '__main__':
    # Run the server in debug mode on host 0.0.0.0 and port 5000.
    app.run(debug=True, host='0.0.0.0', port=5069)
