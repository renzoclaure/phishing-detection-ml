import pandas as pd
import joblib
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import confusion_matrix

def train_and_plot(df, tag):
    X = df.drop(columns=["label"])
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Random Forest
    rf = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        class_weight="balanced",
        n_jobs=-1,
        random_state=42
    )
    rf.fit(X_train, y_train)
    preds_rf = rf.predict(X_test)
    cm_rf = confusion_matrix(y_test, preds_rf)

    plt.figure(figsize=(4,4))
    sns.heatmap(cm_rf, annot=True, fmt="d", cmap="Blues")
    plt.title(f"Confusion Matrix — RF — {tag}")
    plt.savefig(f"report/confusion_matrix_RF_{tag}.png", dpi=300)
    plt.close()

    # XGBoost
    xgb = XGBClassifier(
        n_estimators=600,
        max_depth=8,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        eval_metric="logloss",
        random_state=42
    )
    xgb.fit(X_train, y_train)
    preds_xgb = xgb.predict(X_test)
    cm_xgb = confusion_matrix(y_test, preds_xgb)

    plt.figure(figsize=(4,4))
    sns.heatmap(cm_xgb, annot=True, fmt="d", cmap="Blues")
    plt.title(f"Confusion Matrix — XGB — {tag}")
    plt.savefig(f"report/confusion_matrix_XGB_{tag}.png", dpi=300)
    plt.close()

    print(f"[OK] Confusion matrices generated for: {tag}")


datasets = {
    "full": "data/processed/url_features_dataset_full.csv",
    "balanced": "data/processed/url_features_dataset_balanced.csv",
    "reduced": "data/processed/url_features_dataset_reduced.csv",
}

for tag, path in datasets.items():
    print(f"Processing dataset: {tag}")
    df = pd.read_csv(path)
    train_and_plot(df, tag)
