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
        features (dict): Keys are feature names from dataset (except 'id' and 'CLASS_LABEL').

    Returns:
        dict: {
            "malicious_prob": float probability of being phishing,
            "prediction": "unsafe" or "safe"
        }
    """
    df = pd.DataFrame([features])
    prob = clf.predict_proba(df)[:, 1][0]
    pred = "unsafe" if prob >= threshold else "safe"
    return {"malicious_prob": float(prob), "prediction": pred}

# ----------------------------
# Example usage
# ----------------------------
if __name__ == "__main__":
    # Base feature template (all zeros)
    feature_keys = [
        "NumDots", "SubdomainLevel", "PathLevel", "UrlLength", "NumDash",
        "NumDashInHostname", "AtSymbol", "TildeSymbol", "NumUnderscore",
        "NumPercent", "NumQueryComponents", "NumAmpersand", "NumHash",
        "NumNumericChars", "NoHttps", "RandomString", "IpAddress",
        "DomainInSubdomains", "DomainInPaths", "HttpsInHostname",
        "HostnameLength", "PathLength", "QueryLength", "DoubleSlashInPath",
        "NumSensitiveWords", "EmbeddedBrandName", "PctExtHyperlinks",
        "PctExtResourceUrls", "ExtFavicon", "InsecureForms",
        "RelativeFormAction", "ExtFormAction", "AbnormalFormAction",
        "PctNullSelfRedirectHyperlinks", "FrequentDomainNameMismatch",
        "FakeLinkInStatusBar", "RightClickDisabled", "PopUpWindow",
        "SubmitInfoToEmail", "IframeOrFrame", "MissingTitle",
        "ImagesOnlyInForm", "SubdomainLevelRT", "UrlLengthRT",
        "PctExtResourceUrlsRT", "AbnormalExtFormActionR",
        "ExtMetaScriptLinkRT", "PctExtNullSelfRedirectHyperlinksRT"
    ]

    # Example features: mostly zeros
    example_features = {key: 0 for key in feature_keys}
    example_features.update({
        "NumDots": 3,
        "SubdomainLevel": 2,
        "PathLevel": 1,
        "UrlLength": 50,
        "NumNumericChars": 3,
        "HostnameLength": 12,
        "PathLength": 5
    })

    result = predict_url(example_features)
    print(result)
