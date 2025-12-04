import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score
import joblib

# -----------------------------
# Paths (ajusta si es necesario)
# -----------------------------
FEATURE_FILE = "data/processed/url_features_dataset_full.csv"
MODEL_XGB = "models/modelo_xgb_url_final_full.pkl"
MODEL_RF = "models/modelo_rf_url_final_full.pkl"
OUTPUT = "report/roc_curve_comparison.png"

print("Loading dataset...")
df = pd.read_csv(FEATURE_FILE)

X = df.drop(columns=["label"])
y = df["label"]

print("Loading models...")
model_xgb = joblib.load(MODEL_XGB)
model_rf = joblib.load(MODEL_RF)

print("Generating predictions...")
proba_xgb = model_xgb.predict_proba(X)[:, 1]
proba_rf = model_rf.predict_proba(X)[:, 1]

# -----------------------------
# ROC Curve Computation
# -----------------------------
fpr_xgb, tpr_xgb, _ = roc_curve(y, proba_xgb)
fpr_rf, tpr_rf, _ = roc_curve(y, proba_rf)

auc_xgb = roc_auc_score(y, proba_xgb)
auc_rf = roc_auc_score(y, proba_rf)

print(f"AUC XGBoost: {auc_xgb:.5f}")
print(f"AUC Random Forest: {auc_rf:.5f}")

# -----------------------------
# Plot ROC Curves
# -----------------------------
plt.figure(figsize=(10, 6))

plt.plot(fpr_xgb, tpr_xgb, label=f"XGBoost (AUC = {auc_xgb:.4f})", linewidth=2)
plt.plot(fpr_rf,  tpr_rf,  label=f"Random Forest (AUC = {auc_rf:.4f})", linewidth=2)

plt.plot([0, 1], [0, 1], 'k--', linewidth=1)

plt.title("ROC Curve Comparison: XGBoost vs Random Forest", fontsize=14)
plt.xlabel("False Positive Rate", fontsize=12)
plt.ylabel("True Positive Rate", fontsize=12)
plt.legend(loc="lower right")
plt.grid(True)

plt.tight_layout()
plt.savefig(OUTPUT, dpi=300)
plt.close()

print(f"ROC curve saved to: {OUTPUT}")
