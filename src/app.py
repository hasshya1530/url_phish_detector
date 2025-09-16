# src/app.py
from flask import Flask, request, jsonify
from extract_features import extract_url_features
from predict_url import predict_url

app = Flask(__name__)

@app.route("/")
def home():
    return "URL Phishing Detection API is live!"

@app.route("/predict", methods=["POST"])
def predict():
    """
    Accepts JSON body: {"url": "<URL_TO_CHECK>"}
    Returns JSON: {"url": ..., "malicious_prob": ..., "prediction": ...}
    """
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "Please provide a 'url' in JSON body"}), 400

    url = data["url"]
    features = extract_url_features(url)
    result = predict_url(features)
    result["url"] = url
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
