import logging
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder

# Import your preprocessing functions and feature lists
# Make sure preprocess.py is in the same directory (app/)
from preprocess import engineer_features, numeric_features, categorical_features

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------------------------------------------------
# Load the model (saved with joblib) at startup
# -------------------------------------------------------------------
MODEL_PATH = Path(__file__).parent / "model.pkl"
try:
    model = joblib.load(MODEL_PATH)
    logger.info("Model loaded successfully with joblib")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    raise RuntimeError("Model could not be loaded") from e

# Combine all raw feature names (the ones your model expects after engineer_features)
ALL_FEATURES = numeric_features + categorical_features

# -------------------------------------------------------------------
# FastAPI app
# -------------------------------------------------------------------
app = FastAPI(
    title="House Price Prediction API",
    description="Predict sale price using the best model from training.",
    version="1.0.0"
)

# -------------------------------------------------------------------
# Health check endpoint
# -------------------------------------------------------------------
@app.get("/")
@app.get("/health")
async def health_check():
    return {"status": "ok", "model_loaded": True}

# -------------------------------------------------------------------
# Prediction endpoint – accepts a JSON object with feature values
# -------------------------------------------------------------------
@app.post("/predict")
async def predict(features: dict):
    """
    Expects a JSON object where keys are raw feature names (as in the training CSV)
    and values are the corresponding numbers/strings.
    Example:
    {
        "MSSubClass": 60,
        "MSZoning": "RL",
        "LotFrontage": 65.0,
        ...
    }
    """
    # 1. Validate that all required features are present
    missing = set(ALL_FEATURES) - set(features.keys())
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Missing features: {missing}"
        )

    # 2. Convert to DataFrame (single row)
    try:
        input_df = pd.DataFrame([features])
    except Exception as e:
        logger.error(f"Error creating DataFrame: {e}")
        raise HTTPException(status_code=400, detail="Invalid input format")

    # 3. Apply the same feature engineering that was done during training
    try:
        engineered_df = engineer_features(input_df)
    except Exception as e:
        logger.error(f"Feature engineering failed: {e}")
        raise HTTPException(status_code=500, detail="Error during feature engineering")

    # 4. Make prediction
    try:
        prediction = model.predict(engineered_df)[0]
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed")

    # 5. Return result
    return {"price": float(prediction)}