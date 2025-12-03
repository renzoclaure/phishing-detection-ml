import pandas as pd
from src.url_features import extract_url_features

INPUT = "data/processed/url_labeled_dataset_full.csv"
OUTPUT = "data/processed/url_features_dataset_full.csv"

print("Loading dataset...")
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

print("Feature dataset shape:", feat_df.shape)
feat_df.to_csv(OUTPUT, index=False)
print("Saved to:", OUTPUT)
