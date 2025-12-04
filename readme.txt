# Phishing Detection System using Machine Learning

This project implements a supervised Machine Learning system for detecting phishing URLs using only lexical and structural features. It includes a complete research and deployment pipeline, multiple dataset variants for experimentation, baseline and ensemble models, and a functional web API for real-time classification.

-------------------------------------------------------------------------------
Overview
-------------------------------------------------------------------------------

The project contains two major components:

1. Research Pipeline  
   A full experimental workflow including dataset construction, feature engineering, model training, evaluation across multiple datasets, ROC and Precision–Recall curves, confusion matrices, and training-time analysis.

2. Operational Pipeline  
   A deployable system that exposes a Flask-based REST API and a web interface for real-time phishing detection.

This repository accompanies a scientific report written in IEEE format.

-------------------------------------------------------------------------------
Features
-------------------------------------------------------------------------------

- URL classification using supervised learning.
- Real-time API response with probability scores.
- Extraction of 30 handcrafted lexical, structural, and host-based features.
- Experimental evaluation across:
  - Full dataset (104K URLs)
  - Balanced dataset (10k phishing + 10k legitimate)
  - Reduced-feature dataset (removal of trivial features)
- Comparison of three ML algorithms:
  - Logistic Regression (baseline)
  - Random Forest
  - XGBoost
- Automatic generation of:
  - ROC curves
  - Precision–Recall curves
  - Confusion matrices per dataset
  - Training-time measurements

-------------------------------------------------------------------------------
Installation
-------------------------------------------------------------------------------

Prerequisites:
- Python 3.10+
- Git
- Conda (recommended)

Setup:

git clone <your-repo-url>  
cd phishing_project  

Using Conda:
\`\`\`bash
conda env create -f environment.yaml
conda activate phishing-ml-env
\`\`\`

Using pip:
\`\`\`bash
pip install flask pandas scikit-learn xgboost seaborn joblib tldextract matplotlib
\`\`\`

-------------------------------------------------------------------------------
Usage
-------------------------------------------------------------------------------

Web Application:
\`\`\`bash
cd app
python 4_aplicacion_mlops.py
\`\`\`
Access via http://localhost:5000

REST API:

Prediction endpoint:  
POST /api/predict  
Body: {"url": "https://www.example.com"}

Example:
\`\`\`bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com"}'
\`\`\`

Health Check:
GET /health

-------------------------------------------------------------------------------
Research Pipeline
-------------------------------------------------------------------------------

1. Build the full dataset:
\`\`\`bash
python src/build_url_dataset_full.py
\`\`\`

2. Extract features for the full dataset:
\`\`\`bash
python src/extract_url_features_full.py
\`\`\`

3. Train Random Forest and XGBoost:
\`\`\`bash
python src/train_final_url_model_full.py
\`\`\`

-------------------------------------------------------------------------------
Additional Experimental Datasets
-------------------------------------------------------------------------------

Balanced Dataset:
\`\`\`bash
python src/build_balanced_dataset.py
python src/extract_features_balanced.py
\`\`\`

Reduced-Feature Dataset:
\`\`\`bash
python src/build_reduced_feature_dataset.py
\`\`\`

-------------------------------------------------------------------------------
Analysis Tools
-------------------------------------------------------------------------------

Precision–Recall Curves:
\`\`\`bash
python src/generate_pr_curves.py
\`\`\`

Confusion Matrices (full, balanced, reduced):
\`\`\`bash
python src/generate_confusion_matrices_variants.py
\`\`\`

Training Time Comparison:
\`\`\`bash
python src/measure_training_times.py
\`\`\`

-------------------------------------------------------------------------------
Project Structure
-------------------------------------------------------------------------------

phishing_project/
├── app/
│   ├── 4_aplicacion_mlops.py
│   ├── templates/
│   └── static/
│
├── src/
│   ├── url_features.py
│   ├── build_url_dataset_full.py
│   ├── extract_url_features_full.py
│   ├── train_final_url_model_full.py
│   ├── build_balanced_dataset.py
│   ├── extract_features_balanced.py
│   ├── build_reduced_feature_dataset.py
│   ├── generate_pr_curves.py
│   ├── generate_confusion_matrices_variants.py
│   └── measure_training_times.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│   ├── modelo_xgb_url_final_full.pkl
│   ├── modelo_rf_url_final_full.pkl
│   └── lr.pkl
│
├── report/
│   ├── roc_curve_comparison.png
│   ├── pr_curve_comparison.png
│   ├── confusion_matrix_*.png
│
├── notebooks/
├── FINAL_REPORT_IEEE.pdf
├── environment.yaml
└── README.txt

-------------------------------------------------------------------------------
Technical Details
-------------------------------------------------------------------------------

Extracted Features (30 total):

Lexical:
- URL length  
- Special character counts (@, -, .)  
- Directory depth  
- Digit and symbol patterns  

Host-based:
- IP address usage  
- Subdomain presence and depth  
- TLD composition  

Protocol-level:
- HTTPS flag  
- Redirect indicators  
- Non-standard ports  

Structural:
- Common phishing path/fragment patterns  

Models:

Logistic Regression:
- Baseline linear model

Random Forest:
- 200 trees  
- max_depth = 15  
- class_weight = balanced  

XGBoost:
- 600 estimators  
- max_depth = 8  
- learning_rate = 0.05  
- regularization via subsample and colsample_bytree  

-------------------------------------------------------------------------------
License
-------------------------------------------------------------------------------

This project was developed as part of the Applied Artificial Intelligence Master (2025) — AI for Cybersecurity.
