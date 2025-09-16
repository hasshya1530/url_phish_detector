import requests

API_URL = "https://url-phish-detector-65xb.onrender.com/predict"  # your deployed URL
urls = [
    "https://www.google.com",
    "http://paypal-login.fake.com",
    "https://secure-chase-login.com/account",
    "http://mybank-support.org",
    "https://github.com"
]

for url in urls:
    try:
        response = requests.post(API_URL, json={"url": url})
        response.raise_for_status()
        print(f"URL: {url} -> {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error testing {url}: {e}")
