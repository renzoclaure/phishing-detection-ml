import pandas as pd
import joblib
import time
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score

INPUT = "data/processed/url_features_dataset_full.csv"
OUTPUT = "models/lr.pkl"

df = pd.read_csv(INPUT)

X = df.drop(columns=["label"])
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

start = time.time()
lr = LogisticRegression(max_iter=2000, n_jobs=-1)
lr.fit(X_train, y_train)
end = time.time()

pred = lr.predict(X_test)
proba = lr.predict_proba(X_test)[:, 1]

print("AUC:", roc_auc_score(y_test, proba))
print("ACC:", accuracy_score(y_test, pred))
print("Training time (s):", end - start)

joblib.dump(lr, OUTPUT)
print("Model saved:", OUTPUT)
