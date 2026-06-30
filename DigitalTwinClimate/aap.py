import os

# Prevent OpenBLAS memory issues
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from xgboost import XGBRegressor
import joblib
import pandas as pd

app = FastAPI(
    title="Project PRITHVI Backend",
    version="1.0.0"
)

# -----------------------------
# Load Models
# -----------------------------

rain_model = XGBRegressor()
rain_model.load_model("models/xgboost_rainfall_model.json")

temperature_model = joblib.load("models/temperature_xgboost.pkl")

humidity_model = joblib.load("models/humidity_xgboost.pkl")


# -----------------------------
# Input Models
# -----------------------------

class TemperatureInput(BaseModel):
    latitude: float
    longitude: float
    year: int
    month: int
    day: int
    hour: int
    dayofyear: int


class HumidityInput(BaseModel):
    latitude: float
    longitude: float
    year: int
    month: int
    day: int
    hour: int
    dayofyear: int


class RainfallInput(BaseModel):
    latitude: float
    longitude: float
    year: int
    month: int
    day: int
    hour: int
    dayofyear: int


# -----------------------------
# Home
# -----------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to Project PRITHVI Backend",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "Project PRITHVI Backend",
        "version": "1.0.0"
    }


# -----------------------------
# Temperature Prediction
# -----------------------------

@app.post("/api/v1/predict/temperature")
def predict_temperature(data: TemperatureInput):

    try:

        sample = pd.DataFrame([data.model_dump()])

        prediction = temperature_model.predict(sample)

        return {
            "status": "success",
            "prediction": float(prediction[0])
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# Humidity Prediction
# -----------------------------

@app.post("/api/v1/predict/humidity")
def predict_humidity(data: HumidityInput):

    try:

        sample = pd.DataFrame([data.model_dump()])

        prediction = humidity_model.predict(sample)

        return {
            "status": "success",
            "prediction": float(prediction[0])
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# Rainfall Prediction
# -----------------------------

@app.post("/api/v1/predict/rainfall")
def predict_rainfall(data: RainfallInput):

    try:

        sample = pd.DataFrame([data.model_dump()])

        prediction = rain_model.predict(sample)

        return {
            "status": "success",
            "prediction": float(prediction[0])
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))