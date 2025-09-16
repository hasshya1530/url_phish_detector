# src/test_api.py
import requests
from extract_features import extract_url_features

API_URL = "http://127.0.0.1:5000/predict"

test_urls = [
    "https://www.google.com",
    "http://paypal-login.fake.com",
    "https://secure-chase-login.com/account",
    "http://mybank-support.org",
    "https://github.com"
]

for url in test_urls:
    features = extract_url_features(url)
    response = requests.post(API_URL, json=features)
    print(f"URL: {url} -> {response.json()}")
