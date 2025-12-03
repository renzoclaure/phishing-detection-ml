import pandas as pd
import joblib
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier  # <--- Nuevo algoritmo
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, classification_report, confusion_matrix, accuracy_score

INPUT = "data/processed/url_features_dataset_full.csv"
OUTPUT_XGB = "models/modelo_xgb_url_final_full.pkl"
OUTPUT_RF = "models/modelo_rf_url_final_full.pkl" # <--- Guardaremos ambos para evidencia

print("Loading features...")
df = pd.read_csv(INPUT)

X = df.drop(columns=["label"])
y = df["label"]

# -------------------------------------------------------------------------
# 1. PREPARACIÓN DE DATOS (Común para ambos modelos)
# -------------------------------------------------------------------------
# Usamos la misma semilla (random_state=42) para garantizar que ambos modelos
# ven exactamente las mismas filas en train y test.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

# Cálculo de desbalance para XGBoost
neg = (y_train == 0).sum()
pos = (y_train == 1).sum()
scale_pos_weight = neg / pos
print(f"Data Split: Train={X_train.shape}, Test={X_test.shape}")
print(f"Scale_pos_weight for XGB: {scale_pos_weight:.4f}")

# -------------------------------------------------------------------------
# 2. MODELO 1: XGBOOST
# -------------------------------------------------------------------------
print("\n--- Training XGBoost ---")
model_xgb = XGBClassifier(
    n_estimators=600,
    max_depth=8,
    learning_rate=0.05,
    subsample=0.9,
    colsample_bytree=0.9,
    scale_pos_weight=scale_pos_weight,
    eval_metric="logloss",
    random_state=42
)
model_xgb.fit(X_train, y_train)

# Predicciones XGB
pred_xgb = model_xgb.predict(X_test)
proba_xgb = model_xgb.predict_proba(X_test)[:, 1]

# -------------------------------------------------------------------------
# 3. MODELO 2: RANDOM FOREST (Requisito: Segundo algoritmo)
# -------------------------------------------------------------------------
print("\n--- Training Random Forest ---")
# Usamos class_weight='balanced' para manejar el desbalance igual que scale_pos_weight
model_rf = RandomForestClassifier(
    n_estimators=200,     # Número estándar de árboles
    max_depth=15,         # Limitamos profundidad para evitar overfitting extremo
    class_weight='balanced', # Crucial para tu dataset desbalanceado
    n_jobs=-1,            # Usa todos los núcleos del CPU
    random_state=42
)
model_rf.fit(X_train, y_train)

# Predicciones RF
pred_rf = model_rf.predict(X_test)
proba_rf = model_rf.predict_proba(X_test)[:, 1]

# -------------------------------------------------------------------------
# 4. COMPARACIÓN Y GUARDADO
# -------------------------------------------------------------------------

# Guardamos modelos
joblib.dump(model_xgb, OUTPUT_XGB)
joblib.dump(model_rf, OUTPUT_RF)
print(f"\nModels saved:\n - {OUTPUT_XGB}\n - {OUTPUT_RF}")

# Imprimimos reporte comparativo para el Paper
print("\n" + "="*40)
print("     COMPARATIVE RESULTS (FOR PAPER)")
print("="*40)

auc_xgb = roc_auc_score(y_test, proba_xgb)
acc_xgb = accuracy_score(y_test, pred_xgb)

auc_rf = roc_auc_score(y_test, proba_rf)
acc_rf = accuracy_score(y_test, pred_rf)

print(f"{'Metric':<15} | {'XGBoost':<10} | {'Random Forest':<10}")
print("-" * 43)
print(f"{'ROC-AUC':<15} | {auc_xgb:.5f}    | {auc_rf:.5f}")
print(f"{'Accuracy':<15} | {acc_xgb:.5f}    | {acc_rf:.5f}")
print("-" * 43)

print("\nConfusion Matrix (XGBoost):\n", confusion_matrix(y_test, pred_xgb))
print("\nConfusion Matrix (Random Forest):\n", confusion_matrix(y_test, pred_rf))

print("\nClassification Report (XGBoost):\n", classification_report(y_test, pred_xgb))
print("\nClassification Report (Random Forest):\n", classification_report(y_test, pred_rf))