# 🛡️ Phishing Detector - AI for Cyber Security Project

Machine Learning-based phishing detection system that analyzes URLs to identify malicious websites using an XGBoost model trained on extracted URL features.

## Features

- ✅ Real-time URL analysis
- ✅ Modern and responsive web interface
- ✅ REST API for integrations
- ✅ Automatic extraction of 30 URL features
- ✅ XGBoost model optimized for phishing detection
- ✅ Confidence probability display
- ✅ Extracted features visualization

## Installation

### Prerequisites

- Python 3.10+
- Conda (recommended) or pip

### Installation Steps

1. **Clone the repository**

2. **Create conda environment:**
```bash
conda env create -f environment.yaml
conda activate phishing-ml-env
```

3. **Or install with pip:**
```bash
pip install flask pandas scikit-learn xgboost joblib tldextract
```

4. **Verify the model exists:**
```bash
ls models/modelo_xgb_url_final_full.pkl
```

If the model doesn't exist, you'll need to train it first (see Training section).

## Usage

### Start the Web Application

```bash
cd app
python 4_aplicacion_mlops.py
```

The application will be available at: `http://localhost:5000`

### Using the Web Interface

1. Open your browser at `http://localhost:5000`
2. Enter a URL in the text field (must include http:// or https://)
3. Click "Analyze"
4. You'll see the result with:
   - Classification (Phishing or Legitimate)
   - Confidence percentage
   - Extracted features (expandable)

### Using the API

#### Prediction Endpoint

```bash
curl -X POST http://localhost:5000/predict \
  -F "url=https://www.example.com"
```

Or with JSON:

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com"}'
```

**Response:**
```json
{
  "success": true,
  "url": "https://www.example.com",
  "prediction": "Legitimate",
  "is_phishing": false,
  "confidence": 95.23,
  "features_extracted": 30,
  "features": {
    "UsoIP": 0,
    "URLLargo": 0,
    "HTTPS": 1,
    ...
  }
}
```

#### Health Endpoint

```bash
curl http://localhost:5000/health
```

## Model Training

If you need to train or retrain the model:

1. **Prepare the data:**
```bash
python src/build_url_dataset_full.py
python src/extract_url_features_full.py
```

2. **Train the model:**
```bash
python src/train_final_url_model_full.py
```

The model will be saved to `models/modelo_xgb_url_final_full.pkl`

## Project Structure

```
phishing_project/
├── app/
│   ├── 4_aplicacion_mlops.py      # Main Flask application
│   ├── templates/
│   │   └── index.html              # Web interface
│   └── static/
│       └── styles.css              # CSS styles
├── src/
│   ├── url_features.py             # Feature extraction
│   ├── build_url_dataset_full.py   # Dataset construction
│   ├── extract_url_features_full.py # Feature extraction
│   └── train_final_url_model_full.py # Model training
├── data/
│   ├── raw/                        # Raw data
│   └── processed/                  # Processed data
├── models/
│   └── modelo_xgb_url_final_full.pkl # Trained model
├── notebooks/                       # Jupyter notebooks
├── environment.yaml                 # Conda dependencies
└── README.md                        # This file
```

## Extracted Features

The system extracts 30 features from each URL, including:

- IP address usage instead of domain
- URL length
- Presence of special symbols (@, #, etc.)
- HTTPS usage
- Subdomains
- Redirects
- And more...

## Troubleshooting

### Error: "Model file not found"

Make sure the model exists at `models/modelo_xgb_url_final_full.pkl`. If it doesn't exist, train it first.

### Error: "ModuleNotFoundError: No module named 'tldextract'"

Install the missing dependency:
```bash
pip install tldextract
```

### Error loading the model

Verify that the model was saved correctly with `joblib.dump()`. If you used `save_model()`, you'll need to load it with `XGBClassifier.load_model()`.

## Model Performance

The XGBoost model was trained with:
- 600 estimators
- Maximum depth: 8
- Learning rate: 0.05
- Automatic class balancing

## Security

- URLs are validated before processing
- Errors don't expose sensitive information
- The application validates input format

## License

This project is part of a research thesis.

## Contributions

Improvements and suggestions are welcome. Please review the `ANALISIS_MEJORAS.md` file to see suggested improvements.

## Contact

For questions or issues, please open an issue in the repository.

---

**Note:** This is a research project. Results should not be the sole source of decision-making to determine if a site is safe or not.
