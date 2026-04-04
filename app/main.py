from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "model.joblib"

app = FastAPI(
    title="Boston Housing Prediction API",
    description="API для предсказания medv по признакам Boston Housing",
    version="1.0.0",
)


class HouseFeatures(BaseModel):
    crim: float = Field(..., example=0.02729)
    zn: float = Field(..., example=0.0)
    indus: float = Field(..., example=7.07)
    chas: int = Field(..., example=0)
    nox: float = Field(..., example=0.469)
    rm: float = Field(..., example=7.185)
    age: float = Field(..., example=61.1)
    dis: float = Field(..., example=4.9671)
    rad: int = Field(..., example=2)
    tax: int = Field(..., example=242)
    ptratio: float = Field(..., example=17.8)
    black: float = Field(..., example=392.83)
    lstat: float = Field(..., example=4.03)


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Файл модели не найден: {MODEL_PATH}. "
            f"Сначала запусти src/train.py"
        )
    return joblib.load(MODEL_PATH)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "model_exists": MODEL_PATH.exists()
    }


@app.post("/predict")
def predict(features: HouseFeatures):
    model = load_model()

    input_df = pd.DataFrame([features.model_dump()])
    prediction = float(model.predict(input_df)[0])

    return {
        "predicted_medv": round(prediction, 4)
    }