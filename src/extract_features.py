# src/extract_features.py
import tldextract
import re

def extract_url_features(url: str) -> dict:
    """
    Convert a URL string into numeric features used by the trained model.
    """
    url = url.lower()
    features = {}

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

    # All other features default
    other_features = [
        "NumSensitiveWords","EmbeddedBrandName","PctExtHyperlinks","PctExtResourceUrls",
        "ExtFavicon","InsecureForms","RelativeFormAction","ExtFormAction","AbnormalFormAction",
        "PctNullSelfRedirectHyperlinks","FrequentDomainNameMismatch","FakeLinkInStatusBar",
        "RightClickDisabled","PopUpWindow","SubmitInfoToEmail","IframeOrFrame","MissingTitle",
        "ImagesOnlyInForm","SubdomainLevelRT","UrlLengthRT","PctExtResourceUrlsRT",
        "AbnormalExtFormActionR","ExtMetaScriptLinkRT","PctExtNullSelfRedirectHyperlinksRT"
    ]
    for f in other_features:
        features[f] = 0 if "Pct" not in f else 0.0

    return features
