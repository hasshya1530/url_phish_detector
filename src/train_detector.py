# src/train_detector.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, precision_recall_curve, auc
import joblib
import os

# Load dataset
df = pd.read_csv("data/phishing_dataset.csv")  # replace with your file name

# Features and label
X = df.drop(columns=['id', 'CLASS_LABEL'])
y = df['CLASS_LABEL'].values

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Train Logistic Regression + Calibration
clf = LogisticRegression(max_iter=1000, class_weight='balanced', solver='saga')
calibrated = CalibratedClassifierCV(clf, method='sigmoid', cv=3)
calibrated.fit(X_train, y_train)

# Evaluate
y_prob = calibrated.predict_proba(X_test)[:,1]
y_pred = (y_prob >= 0.5).astype(int)

print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("ROC AUC:", roc_auc_score(y_test, y_prob))

# Determine threshold for precision >= 0.9
precision, recall, thresholds = precision_recall_curve(y_test, y_prob)
target_precision = 0.9
ix = [i for i, p in enumerate(precision) if p >= target_precision]

if ix:
    idx = min(ix[-1], len(thresholds)-1)
    suggested_threshold = thresholds[idx]
else:
    suggested_threshold = 0.5

print(f"Suggested threshold for precision >= {target_precision}: {suggested_threshold:.3f}")


# Save model and threshold
os.makedirs("../models", exist_ok=True)
joblib.dump(calibrated, "../models/calibrated_clf.joblib")
joblib.dump(suggested_threshold, "../models/suggested_threshold.joblib")

print("✅ Model and threshold saved in models/")
