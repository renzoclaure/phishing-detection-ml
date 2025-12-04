import time
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

df = pd.read_csv("data/processed/url_features_dataset_full.csv")

X = df.drop(columns=["label"])
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

models = {
    "LR": LogisticRegression(max_iter=2000, n_jobs=-1),
    "RF": RandomForestClassifier(n_estimators=200, max_depth=15, class_weight="balanced", n_jobs=-1),
    "XGB": XGBClassifier(
        n_estimators=600, max_depth=8, learning_rate=0.05,
        subsample=0.9, colsample_bytree=0.9, eval_metric="logloss"
    )
}

for name, model in models.items():
    start = time.time()
    model.fit(X_train, y_train)
    end = time.time()
    print(f"{name} training time: {end - start:.3f} seconds")
