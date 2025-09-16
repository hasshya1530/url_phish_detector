# src/app.py
from flask import Flask, request, jsonify
from src.extract_features import extract_url_features
from src.predict_url import predict_url

app = Flask(__name__)

@app.route("/")
def index():
    return "URL Phishing Detector API is live!"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "Please provide a 'url' in JSON body"}), 400

    url = data["url"]
    features = extract_url_features(url)
    result = predict_url(features)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
