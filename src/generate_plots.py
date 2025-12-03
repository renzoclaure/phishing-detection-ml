import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

# Configuración visual sobria (estilo paper)
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 12, 'font.family': 'sans-serif'})

# Cargar datos y modelos
INPUT = "data/processed/url_features_dataset_full.csv"
MODEL_XGB = "models/modelo_xgb_url_final_full.pkl"
MODEL_RF = "models/modelo_rf_url_final_full.pkl"

print("Cargando datos y modelos...")
df = pd.read_csv(INPUT)
xgb_model = joblib.load(MODEL_XGB)
rf_model = joblib.load(MODEL_RF)

X = df.drop(columns=["label"])
y = df["label"]

# Mismo split que en entrenamiento
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

# Predicciones
y_pred_xgb = xgb_model.predict(X_test)
y_pred_rf = rf_model.predict(X_test)

# --- GRÁFICO 1: Matriz de Confusión Comparativa ---
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

cm_xgb = confusion_matrix(y_test, y_pred_xgb)
cm_rf = confusion_matrix(y_test, y_pred_rf)

# Plot XGB
sns.heatmap(cm_xgb, annot=True, fmt='d', cmap='Blues', ax=axes[0], cbar=False)
axes[0].set_title('XGBoost Confusion Matrix')
axes[0].set_ylabel('True Label')
axes[0].set_xlabel('Predicted Label')
axes[0].set_xticklabels(['Legit', 'Phishing'])
axes[0].set_yticklabels(['Legit', 'Phishing'])

# Plot RF
sns.heatmap(cm_rf, annot=True, fmt='d', cmap='Greens', ax=axes[1], cbar=False)
axes[1].set_title('Random Forest Confusion Matrix')
axes[1].set_ylabel('') # Ocultar para limpieza
axes[1].set_xlabel('Predicted Label')
axes[1].set_xticklabels(['Legit', 'Phishing'])
axes[1].set_yticklabels(['Legit', 'Phishing'])

plt.tight_layout()
plt.savefig("report/confusion_matrix_comparison.png", dpi=300)
print("Gráfico 1 guardado: report/confusion_matrix_comparison.png")

# --- GRÁFICO 2: Feature Importance (Solo XGBoost para simplificar) ---
plt.figure(figsize=(10, 8))
# Obtener importancia
importance = xgb_model.feature_importances_
feature_names = X.columns
# Crear DataFrame para ordenar
feat_df = pd.DataFrame({'Feature': feature_names, 'Importance': importance})
feat_df = feat_df.sort_values(by='Importance', ascending=False).head(15) # Top 15

sns.barplot(x='Importance', y='Feature', data=feat_df, color="#34495e")
plt.title('Top 15 Most Discriminative Features (XGBoost)')
plt.xlabel('Relative Importance Gain')
plt.ylabel('Feature Name')

plt.tight_layout()
plt.savefig("report/feature_importance.png", dpi=300)
print("Gráfico 2 guardado: report/feature_importance.png")