import pickle
import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conlist
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the model at startup
MODEL_PATH = Path(__file__).parent / "model.pkl"
try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    raise RuntimeError("Model could not be loaded") from e

app = FastAPI(title="House Price Prediction API", version="1.0.0")

# Define request and response schemas
class Features(BaseModel):
    # Example features: adjust according to your model's training features
    MedInc: float          # median income in block
    HouseAge: float        # median house age in block
    AveRooms: float        # average number of rooms
    AveBedrms: float       # average number of bedrooms
    Population: float      # block population
    AveOccup: float        # average house occupancy
    Latitude: float
    Longitude: float

    # Optional: add validators to constrain inputs
    # @validator('MedInc')
    # def check_positive(cls, v):
    #     if v <= 0:
    #         raise ValueError('MedInc must be positive')
    #     return v

class PredictionOut(BaseModel):
    price: float

# Health check endpoint
@app.get("/")
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Prediction endpoint
@app.post("/predict", response_model=PredictionOut)
def predict(features: Features):
    try:
        # Convert input to numpy array (order must match training)
        input_array = np.array([[
            features.MedInc,
            features.HouseAge,
            features.AveRooms,
            features.AveBedrms,
            features.Population,
            features.AveOccup,
            features.Latitude,
            features.Longitude
        ]])
        
        # Make prediction
        prediction = model.predict(input_array)[0]
        
        # Return as float
        return PredictionOut(price=float(prediction))
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed")