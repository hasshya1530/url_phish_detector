from flask import Flask, request, jsonify
import logging
from .predict_url import predict_url

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO)

@app.route("/")
def home():
    return "URL Phishing Detector API is running!"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    logging.info(f"Received data: {data}")

    if not data:
        return jsonify({"error": "No data provided"}), 400

    result = predict_url(data)
    logging.info(f"Prediction result: {result}")

    return jsonify(result)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
