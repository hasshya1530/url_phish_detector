# src/predict_url.py
import os
import joblib
import pandas as pd

# ----------------------------
# Project root path
# ----------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(PROJECT_ROOT, "models")

# ----------------------------
# Load model and threshold
# ----------------------------
clf_path = os.path.join(MODEL_DIR, "calibrated_clf.joblib")
threshold_path = os.path.join(MODEL_DIR, "suggested_threshold.joblib")

if not os.path.exists(clf_path) or not os.path.exists(threshold_path):
    raise FileNotFoundError(
        f"Model files not found in {MODEL_DIR}. Make sure 'calibrated_clf.joblib' "
        "and 'suggested_threshold.joblib' exist."
    )

clf = joblib.load(clf_path)
threshold = joblib.load(threshold_path)

# ----------------------------
# Prediction function
# ----------------------------
def predict_url(features: dict):
    """
    Predict whether a URL is phishing or not based on feature dictionary.

    Args:
        features (dict): Keys are feature names.

    Returns:
        dict: {
            "malicious_prob": float probability of being phishing,
            "prediction": "malicious" or "safe"
        }
    """
    df = pd.DataFrame([features])
    prob = clf.predict_proba(df)[:, 1][0]
    pred = "malicious" if prob >= threshold else "safe"
    return {"malicious_prob": float(prob), "prediction": pred}

if __name__ == "__main__":
    # Example
    from extract_features import extract_url_features
    url = "https://www.google.com"
    features = extract_url_features(url)
    result = predict_url(features)
    print(result)
