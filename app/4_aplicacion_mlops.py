import sys
import os
import logging
from typing import Tuple
from urllib.parse import urlparse

# Get the project root directory (one level above app/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_DIR = os.path.dirname(os.path.abspath(__file__))

# Add project root to path for imports
sys.path.insert(0, PROJECT_ROOT)

from flask import Flask, request, render_template, jsonify
import pandas as pd
import joblib
import xgboost as xgb

from src.url_features import extract_url_features

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Flask with absolute paths for templates and static files
app = Flask(
    __name__,
    template_folder=os.path.join(APP_DIR, 'templates'),
    static_folder=os.path.join(APP_DIR, 'static')
)

# Load model - use absolute path based on project root directory
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "modelo_xgb_url_final_full.pkl")

# Try to load the model
model = None
try:
    if os.path.exists(MODEL_PATH):
        model = xgb.XGBClassifier()
        model.load_model(MODEL_PATH)
        logger.info("Model loaded successfully (XGBoost Booster) from %s", MODEL_PATH)
    else:
        # Try alternative paths
        alt_paths = [
            os.path.join(os.getcwd(), "models", "modelo_xgb_url_final_full.pkl"),
            os.path.join(APP_DIR, "..", "models", "modelo_xgb_url_final_full.pkl"),
            "models/modelo_xgb_url_final_full.pkl"
        ]

        for alt_path in alt_paths:
            abs_alt_path = os.path.abspath(alt_path)
            if os.path.exists(abs_alt_path):
                model = joblib.load(abs_alt_path)
                logger.info("Model loaded successfully from alternative path: %s", abs_alt_path)
                break

        if model is None:
            logger.error("Model file not found. Tried:")
            logger.error("  Primary: %s", MODEL_PATH)
            for alt_path in alt_paths:
                logger.error("  Alternative: %s", os.path.abspath(alt_path))
            logger.error("Current working directory: %s", os.getcwd())
            logger.error("Project root: %s", PROJECT_ROOT)
            logger.error("App directory: %s", APP_DIR)

except (IOError, OSError, ValueError, ImportError) as e:
    logger.error("Error loading model: %s", str(e), exc_info=True)
    model = None


def validate_url(url: str) -> Tuple[bool, str]:
    """Validate that the URL has a valid format."""
    if not url or not isinstance(url, str):
        return False, "Empty or invalid URL"

    url = url.strip()
    if not url:
        return False, "Empty URL"

    # Validate basic URL format
    try:
        result = urlparse(url)
        if not result.scheme or not result.netloc:
            return False, "URL must include protocol (http:// or https://) and domain"
    except (ValueError, TypeError) as e:
        return False, f"Error parsing URL: {str(e)}"

    return True, "OK"


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    """Endpoint to predict if a URL is phishing or legitimate."""
    if model is None:
        return jsonify({
            "error": "Model not available. Please check the configuration.",
            "success": False
        }), 500

    try:
        # Get URL from form or JSON
        if request.is_json:
            data = request.get_json()
            url = data.get("url") or data.get("Url")
        else:
            url = request.form.get("url") or request.form.get("Url")

        if not url:
            return jsonify({
                "error": "No URL provided",
                "success": False
            }), 400

        # Validate URL
        is_valid, message = validate_url(url)
        if not is_valid:
            return jsonify({
                "error": message,
                "success": False
            }), 400

        # Extract features
        feats = extract_url_features(url)
        logger.info("URL analyzed: %s", url)
        logger.debug("Features extracted: %d features", len(feats))

        # Create DataFrame with correct column order
        # Get columns from model if possible
        try:
            # Try to get feature names from XGBoost model
            if hasattr(model, 'get_booster'):
                feature_names = model.get_booster().feature_names
                if feature_names:
                    X = pd.DataFrame([feats], columns=feature_names)
                else:
                    X = pd.DataFrame([feats])
            else:
                X = pd.DataFrame([feats])
        except (AttributeError, KeyError, ValueError):
            # Fallback: use dictionary order
            X = pd.DataFrame([feats])

        # Make prediction
        pred = model.predict(X)[0]
        proba = model.predict_proba(X)[0]

        # Determine result
        is_phishing = pred == 1
        confidence = float(proba[1] if is_phishing else proba[0])
        label = "Phishing" if is_phishing else "Legitimate"

        # Prepare response
        response = {
            "success": True,
            "url": url,
            "prediction": label,
            "is_phishing": bool(is_phishing),
            "confidence": round(confidence * 100, 2),
            "features_extracted": len(feats),
            "features": feats
        }

        return jsonify(response)

    except (ValueError, TypeError, KeyError) as e:
        logger.error("Error in prediction: %s", str(e), exc_info=True)
        return jsonify({
            "error": f"Error processing request: {str(e)}",
            "success": False
        }), 500


@app.route("/api/predict", methods=["POST"])
def api_predict():
    """Alternative API endpoint that accepts JSON."""
    return predict()


@app.route("/health", methods=["GET"])
def health():
    """Health endpoint to check if the application is running."""
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "model_path": MODEL_PATH if model is not None else None
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("DEBUG", "True").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
