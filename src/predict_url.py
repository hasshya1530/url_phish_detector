import os
import joblib
import pandas as pd

# Base directory of current file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load trained model and threshold from models folder
clf = joblib.load(os.path.join(BASE_DIR, "../models/calibrated_clf.joblib"))
threshold = joblib.load(os.path.join(BASE_DIR, "../models/suggested_threshold.joblib"))

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
    # Convert single row to DataFrame
    df = pd.DataFrame([features])

    # Predict probability
    prob = clf.predict_proba(df)[:, 1][0]

    # Apply threshold
    pred = "unsafe" if prob >= threshold else "safe"

    return {"malicious_prob": float(prob), "prediction": pred}

# Example usage
if __name__ == "__main__":
    example_features = {
        "NumDots": 3,
        "SubdomainLevel": 2,
        "PathLevel": 1,
        "UrlLength": 50,
        "NumDash": 1,
        "NumDashInHostname": 0,
        "AtSymbol": 0,
        "TildeSymbol": 0,
        "NumUnderscore": 0,
        "NumPercent": 0,
        "NumQueryComponents": 0,
        "NumAmpersand": 0,
        "NumHash": 0,
        "NumNumericChars": 3,
        "NoHttps": 0,
        "RandomString": 0,
        "IpAddress": 0,
        "DomainInSubdomains": 0,
        "DomainInPaths": 0,
        "HttpsInHostname": 0,
        "HostnameLength": 12,
        "PathLength": 5,
        "QueryLength": 0,
        "DoubleSlashInPath": 0,
        "NumSensitiveWords": 0,
        "EmbeddedBrandName": 0,
        "PctExtHyperlinks": 0.0,
        "PctExtResourceUrls": 0.0,
        "ExtFavicon": 0,
        "InsecureForms": 0,
        "RelativeFormAction": 0,
        "ExtFormAction": 0,
        "AbnormalFormAction": 0,
        "PctNullSelfRedirectHyperlinks": 0.0,
        "FrequentDomainNameMismatch": 0,
        "FakeLinkInStatusBar": 0,
        "RightClickDisabled": 0,
        "PopUpWindow": 0,
        "SubmitInfoToEmail": 0,
        "IframeOrFrame": 0,
        "MissingTitle": 0,
        "ImagesOnlyInForm": 0,
        "SubdomainLevelRT": 0,
        "UrlLengthRT": 0,
        "PctExtResourceUrlsRT": 0.0,
        "AbnormalExtFormActionR": 0,
        "ExtMetaScriptLinkRT": 0.0,
        "PctExtNullSelfRedirectHyperlinksRT": 0.0
    }

    result = predict_url(example_features)
    print(result)
