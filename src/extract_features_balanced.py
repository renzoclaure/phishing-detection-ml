import pandas as pd
import os
import sys

# Add src/ folder to PYTHONPATH dynamically
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

from url_features import extract_url_features  # now works

INPUT = "data/processed/url_labeled_dataset_balanced.csv"
OUTPUT = "data/processed/url_features_dataset_balanced.csv"

print("Loading balanced URL dataset...")
df = pd.read_csv(INPUT)

features = []
labels = []

print("Extracting features from", len(df), "URLs...")

for url, label in zip(df["url"], df["label"]):
    feats = extract_url_features(url)
    features.append(feats)
    labels.append(label)

feat_df = pd.DataFrame(features)
feat_df["label"] = labels

print("Balanced feature dataset shape:", feat_df.shape)
feat_df.to_csv(OUTPUT, index=False)
print("Saved to:", OUTPUT)
