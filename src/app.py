import os
import joblib
import numpy as np
import pandas as pd
import scipy.sparse as sp

# Load models
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

calibrated_path = os.path.join(BASE_DIR, "../models/calibrated_clf.joblib")
threshold_path = os.path.join(BASE_DIR, "../models/suggested_threshold.joblib")
lex_cols_path = os.path.join(BASE_DIR, "../models/lex_cols.joblib")

calibrated = joblib.load(calibrated_path)
suggested_threshold = joblib.load(threshold_path)
lex_cols = joblib.load(lex_cols_path)

# Feature extraction
def extract_features(url_features: dict):
    # url_features: dictionary of numeric features
    lex_features = np.array([[url_features.get(col, 0) for col in lex_cols]])
    return lex_features

# Prediction
def predict_url(url_features: dict):
    X = extract_features(url_features)
    prob = calibrated.predict_proba(X)[:, 1][0]
    pred_label = "unsafe" if prob >= suggested_threshold else "safe"
    return {"malicious_prob": float(prob), "prediction": pred_label}
