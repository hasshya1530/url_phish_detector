# src/app.py
from flask import Flask, request, jsonify
import os
import sys

# Add src folder to path so we can import predict_url
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
sys.path.append(SRC_DIR)

from predict_url import predict_url

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "URL Phishing Detector API is running!"})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if not data or "features" not in data:
        return jsonify({"error": "Please provide a 'features' dictionary in JSON body"}), 400

    features = data["features"]
    try:
        result = predict_url(features)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
