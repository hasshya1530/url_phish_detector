# src/app.py
import os
from flask import Flask, request, jsonify
from predict_url import predict_url

app = Flask(__name__)

@app.route('/')
def home():
    return "URL Phishing Detector API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    if not data:
        return jsonify({'error': 'No input provided'}), 400
    try:
        result = predict_url(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
