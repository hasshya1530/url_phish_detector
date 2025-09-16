# URL Phishing Detector

A Python-based machine learning system to detect phishing URLs using a trained Random Forest classifier. Provides both a Python API and a REST API for easy integration.

---

## Features

- Detects whether a URL is **safe** or **malicious**.
- Uses a trained **Random Forest model** with calibrated probabilities.
- Returns both probability and prediction in JSON format:
  ```json
  {
    "malicious_prob": 0.93,
    "prediction": "unsafe"
  }
