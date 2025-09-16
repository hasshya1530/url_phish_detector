# src/app.py
from flask import Flask, request, jsonify
from extract_features import extract_url_features
from predict_url import predict_url

app = Flask(__name__)

@app.route("/")
def home():
    return "URL Phishing Detector API is running!"

@app.route("/predict", methods=["POST"])
def predict():
    """
    Accepts a JSON body with a 'url' key.
    Example:
    {
        "url": "https://www.google.com"
    }
    """
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "Please provide a 'url' in JSON body"}), 400

    url = data["url"]
    
    try:
        # Extract features from the URL
        features = extract_url_features(url)
        # Predict safe/unsafe
        result = predict_url(features)
        result["url"] = url
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
