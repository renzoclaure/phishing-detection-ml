import pandas as pd

PHISH_PATH = "data/raw/phishtank/phishing_urls.csv"
LEGIT_PATH = "data/raw/alexa/legit_urls.csv"
OUTPUT = "data/processed/url_labeled_dataset_full.csv"

print("Loading phishing data...")
phish = pd.read_csv(PHISH_PATH)
print("Phishing count:", len(phish))

print("Loading legitimate data...")
legit = pd.read_csv(LEGIT_PATH)
print("Legitimate count:", len(legit))

# Combine without balancing
df = pd.concat([phish, legit], ignore_index=True)

print("\nCombined dataset size:", len(df))
print(df['label'].value_counts())

df.to_csv(OUTPUT, index=False)
print("Saved full dataset to:", OUTPUT)
