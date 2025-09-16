# src/predict_url.py
import os
import joblib
import pandas as pd

clf = None
threshold = None

def load_model():
    """Lazy-load model and threshold only once."""
    global clf, threshold
    if clf is None or threshold is None:
        MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
        clf_path = os.path.join(MODEL_DIR, "calibrated_clf.joblib")
        threshold_path = os.path.join(MODEL_DIR, "suggested_threshold.joblib")

        if not os.path.exists(clf_path) or not os.path.exists(threshold_path):
            raise FileNotFoundError(
                f"Model files not found in {MODEL_DIR}. "
                "Make sure 'calibrated_clf.joblib' and 'suggested_threshold.joblib' exist."
            )

        clf = joblib.load(clf_path)
        threshold = joblib.load(threshold_path)

def predict_url(features: dict):
    """
    Predict whether a URL is safe or malicious based on extracted features.
    """
    load_model()
    df = pd.DataFrame([features])
    prob = clf.predict_proba(df)[:, 1][0]
    pred = "malicious" if prob >= threshold else "safe"
    return {"malicious_prob": float(prob), "prediction": pred}
