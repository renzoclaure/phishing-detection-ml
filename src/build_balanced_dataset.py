import pandas as pd

INPUT = "data/processed/url_labeled_dataset_full.csv"
OUTPUT = "data/processed/url_labeled_dataset_balanced.csv"

df = pd.read_csv(INPUT)

phish = df[df["label"] == 1]
legit = df[df["label"] == 0]

n = len(legit)

phish_bal = phish.sample(n, random_state=42)

balanced = pd.concat([phish_bal, legit], ignore_index=True).sample(frac=1, random_state=42)

balanced.to_csv(OUTPUT, index=False)

print("Balanced dataset created:", balanced.shape)
print(balanced['label'].value_counts())
