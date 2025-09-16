import pandas as pd

# Load the dataset
df = pd.read_csv("data/phishing_dataset.csv")  # replace with your exact file name

# Preview first few rows
print(df.head())

# Check column names
print(df.columns)

# Check distribution of labels
print(df['CLASS_LABEL'].value_counts())  # replace 'Label' with your actual label column
