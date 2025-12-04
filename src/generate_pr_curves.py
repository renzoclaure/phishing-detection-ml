import pandas as pd
import joblib
from sklearn.metrics import precision_recall_curve
import matplotlib.pyplot as plt

df = pd.read_csv("data/processed/url_features_dataset_full.csv")
X = df.drop(columns=["label"])
y = df["label"]

models = {
    "LR": joblib.load("models/lr.pkl"),
    "RF": joblib.load("models/modelo_rf_url_final_full.pkl"),
    "XGB": joblib.load("models/modelo_xgb_url_final_full.pkl")
}

plt.figure(figsize=(8,6))

for name, model in models.items():
    proba = model.predict_proba(X)[:,1]
    p, r, _ = precision_recall_curve(y, proba)
    plt.plot(r, p, label=name)

plt.xlabel("Recall")
plt.ylabel("Precision")
plt.title("Precision–Recall Curves")
plt.legend()
plt.grid()
plt.savefig("report/pr_curve_comparison.png", dpi=300)
plt.close()

print("Saved PR Curve to report/pr_curve_comparison.png")
