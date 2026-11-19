
from pathlib import Path

import joblib
import pandas as pd

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.database import (
    SessionLocal,
    PredictionRecord,
    initialize_database
)

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "isolation_forest.joblib"

app = FastAPI(
    title="LogLens AI API",
    description="Machine Learning API for server anomaly detection",
    version="2.0.0"
)

model = None

if MODEL_PATH.exists():
    model = joblib.load(MODEL_PATH)

initialize_database()


class ServerMetrics(BaseModel):
    cpu_usage: float = Field(ge=0, le=100)
    memory_usage: float = Field(ge=0, le=100)
    response_time_ms: float = Field(ge=0)
    network_traffic_mb: float = Field(ge=0)


@app.get("/")
def home():
    return {
        "message": "Welcome to LogLens AI API",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "database": "initialized"
    }


@app.post("/predict")
def predict(metrics: ServerMetrics):

    if model is None:
        raise HTTPException(
            status_code=503,
            detail="ML model not found. Train the model first."
        )

    input_data = pd.DataFrame([{
        "cpu_usage": metrics.cpu_usage,
        "memory_usage": metrics.memory_usage,
        "response_time_ms": metrics.response_time_ms,
        "network_traffic_mb": metrics.network_traffic_mb
    }])

    prediction = int(model.predict(input_data)[0])
    anomaly_score = float(model.decision_function(input_data)[0])

    is_anomaly = prediction == -1
    prediction_label = "ANOMALY" if is_anomaly else "NORMAL"

    db = SessionLocal()

    try:
        record = PredictionRecord(
            cpu_usage=metrics.cpu_usage,
            memory_usage=metrics.memory_usage,
            response_time_ms=metrics.response_time_ms,
            network_traffic_mb=metrics.network_traffic_mb,
            prediction=prediction_label,
            is_anomaly=is_anomaly,
            anomaly_score=anomaly_score
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        return {
            "project": "LogLens AI",
            "prediction_id": record.id,
            "prediction": prediction_label,
            "is_anomaly": is_anomaly,
            "anomaly_score": round(anomaly_score, 5),
            "database_status": "saved",
            "input_metrics": metrics.model_dump()
        }

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to save prediction to database."
        )

    finally:
        db.close()
@app.get("/history")
def get_prediction_history(limit: int = 50):
    if limit < 1 or limit > 500:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 500."
        )

    db = SessionLocal()

    try:
        records = (
            db.query(PredictionRecord)
            .order_by(PredictionRecord.id.desc())
            .limit(limit)
            .all()
        )

        return {
            "project": "LogLens AI",
            "total_records": len(records),
            "history": [
                {
                    "id": record.id,
                    "timestamp": (
                        record.timestamp.isoformat()
                        if record.timestamp else None
                    ),
                    "cpu_usage": record.cpu_usage,
                    "memory_usage": record.memory_usage,
                    "response_time_ms": record.response_time_ms,
                    "network_traffic_mb": record.network_traffic_mb,
                    "prediction": record.prediction,
                    "is_anomaly": record.is_anomaly,
                    "anomaly_score": record.anomaly_score
                }
                for record in records
            ]
        }

    finally:
        db.close()