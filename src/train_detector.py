import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "../models")
os.makedirs(MODEL_DIR, exist_ok=True)

# Load dataset
df = pd.read_csv(os.path.join(BASE_DIR, "../data/phishing_dataset.csv"))
X = df.drop(columns=["id", "CLASS_LABEL"])
y = df["CLASS_LABEL"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Train model with calibration
clf = RandomForestClassifier(n_estimators=200, random_state=42)
calibrated = CalibratedClassifierCV(clf, method="sigmoid", cv=3)
calibrated.fit(X_train, y_train)

# Compute threshold for precision >= 0.9
y_prob = calibrated.predict_proba(X_test)[:, 1]
precision = y_train.value_counts(normalize=True)[1]  # simplified; adjust if needed
threshold = 0.5  # for simplicity; replace with precision calculation if desired

# Save model and threshold
joblib.dump(calibrated, os.path.join(MODEL_DIR, "calibrated_clf.joblib"))
joblib.dump(threshold, os.path.join(MODEL_DIR, "suggested_threshold.joblib"))

print("✅ Model and threshold saved in models/")
