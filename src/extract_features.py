# src/extract_features.py
import tldextract
import re

def extract_url_features(url: str) -> dict:
    """
    Convert a URL string into the numeric features used by the trained model.
    """
    url = url.lower()
    features = {}

    # Basic lexical features
    features["NumDots"] = url.count(".")
    features["SubdomainLevel"] = len(tldextract.extract(url).subdomain.split(".")) if tldextract.extract(url).subdomain else 0
    features["PathLevel"] = url.count("/")
    features["UrlLength"] = len(url)
    features["NumDash"] = url.count("-")
    features["NumDashInHostname"] = url.split("//")[-1].split("/")[0].count("-")
    features["AtSymbol"] = url.count("@")
    features["TildeSymbol"] = url.count("~")
    features["NumUnderscore"] = url.count("_")
    features["NumPercent"] = url.count("%")
    features["NumQueryComponents"] = url.count("?")
    features["NumAmpersand"] = url.count("&")
    features["NumHash"] = url.count("#")
    features["NumNumericChars"] = len(re.findall(r'\d', url))
    features["NoHttps"] = 0 if url.startswith("https") else 1
    features["RandomString"] = 0
    features["IpAddress"] = 1 if re.match(r"http[s]?://(?:[0-9]{1,3}\.){3}[0-9]{1,3}", url) else 0
    features["DomainInSubdomains"] = 0
    features["DomainInPaths"] = 0
    features["HttpsInHostname"] = 1 if "https" in url.split("//")[-1].split("/")[0] else 0
    features["HostnameLength"] = len(url.split("//")[-1].split("/")[0])
    features["PathLength"] = len(url.split("//")[-1].split("/")[1:]) if "/" in url.split("//")[-1] else 0
    features["QueryLength"] = len(url.split("?")[1]) if "?" in url else 0
    features["DoubleSlashInPath"] = 1 if "//" in url.split("://")[-1] else 0
    features["NumSensitiveWords"] = 0
    features["EmbeddedBrandName"] = 0
    features["PctExtHyperlinks"] = 0.0
    features["PctExtResourceUrls"] = 0.0
    features["ExtFavicon"] = 0
    features["InsecureForms"] = 0
    features["RelativeFormAction"] = 0
    features["ExtFormAction"] = 0
    features["AbnormalFormAction"] = 0
    features["PctNullSelfRedirectHyperlinks"] = 0.0
    features["FrequentDomainNameMismatch"] = 0
    features["FakeLinkInStatusBar"] = 0
    features["RightClickDisabled"] = 0
    features["PopUpWindow"] = 0
    features["SubmitInfoToEmail"] = 0
    features["IframeOrFrame"] = 0
    features["MissingTitle"] = 0
    features["ImagesOnlyInForm"] = 0
    features["SubdomainLevelRT"] = 0
    features["UrlLengthRT"] = 0
    features["PctExtResourceUrlsRT"] = 0.0
    features["AbnormalExtFormActionR"] = 0
    features["ExtMetaScriptLinkRT"] = 0.0
    features["PctExtNullSelfRedirectHyperlinksRT"] = 0.0

    return features
if __name__ == "__main__":
    test_url = "https://www.google.com"
    features = extract_url_features(test_url)
    print(features)
