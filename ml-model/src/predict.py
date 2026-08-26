import os
import joblib
import pandas as pd
import numpy as np
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# 1. Define Request / Response Schemas (Matching Section 4 & 5 Contracts)
class LocationCandidate(BaseModel):
    location_id: str
    latitude: float
    longitude: float
    prediction_time: str
    crime_category: str
    transaction_amount: float
    recent_txn_count: int
    recent_withdrawal_count: int
    distance_to_recent_withdrawal_km: float
    historical_location_risk: float
    hour: int
    day_of_week: int

class PredictRequest(BaseModel):
    candidates: List[LocationCandidate]
    predicted_window: Optional[str] = "3h"

class PredictionResult(BaseModel):
    prediction_id: str
    location_id: str
    risk_score: float
    risk_level: str
    predicted_window: str
    rank: int
    top_factors: List[str]
    model_version: str

class PredictResponse(BaseModel):
    status: str
    count: int
    predictions: List[PredictionResult]

# 2. Initialize App and Load Model
app = FastAPI(title="Cybercrime Withdrawal Hotspot Predictor")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}. Run src/train.py first.")

artifact = joblib.load(MODEL_PATH)
model = artifact['model']
expected_columns = artifact['feature_names']
model_version = artifact.get('model_version', 'rf_v1')

def get_risk_level(score: float) -> str:
    """Map continuous risk score to categorical levels."""
    if score >= 0.75:
        return "CRITICAL"
    elif score >= 0.50:
        return "HIGH"
    elif score >= 0.25:
        return "MEDIUM"
    return "LOW"

# 3. Prediction Endpoint
@app.post("/predict", response_model=PredictResponse)
def predict_hotspots(payload: PredictRequest):
    if not payload.candidates:
        raise HTTPException(status_code=400, detail="Candidate list is empty")

    # Convert request objects to DataFrame
    input_data = [c.dict() for c in payload.candidates]
    df_raw = pd.DataFrame(input_data)

    # Feature transformation & alignment
    feature_cols = [
        'latitude', 'longitude', 'crime_category', 'transaction_amount',
        'recent_txn_count', 'recent_withdrawal_count',
        'distance_to_recent_withdrawal_km', 'historical_location_risk',
        'hour', 'day_of_week'
    ]
    
    X_encoded = pd.get_dummies(df_raw[feature_cols], drop_first=True)
    X_aligned = X_encoded.reindex(columns=expected_columns, fill_value=0)

    # Predict Probabilities
    scores = model.predict_proba(X_aligned)[:, 1]

    # Global feature importances for explainability factors
    if hasattr(model, "feature_importances_"):
        top_global_factors = [
            expected_columns[i] 
            for i in np.argsort(model.feature_importances_)[::-1][:3]
        ]
    else:
        top_global_factors = ["recent_withdrawal_count", "distance_to_recent_withdrawal_km", "historical_location_risk"]

    # Build results and assign rank
    results = []
    for idx, row in df_raw.iterrows():
        score = float(scores[idx])
        results.append({
            "location_id": row["location_id"],
            "risk_score": round(score, 4),
            "risk_level": get_risk_level(score),
            "predicted_window": payload.predicted_window,
            "top_factors": top_global_factors,
            "model_version": model_version
        })

    # Sort descending by risk score for hotspot ranking
    results.sort(key=lambda x: x["risk_score"], reverse=True)

    # Add ranks and prediction IDs
    formatted_predictions = []
    for rank_idx, item in enumerate(results, start=1):
        formatted_predictions.append(
            PredictionResult(
                prediction_id=f"pred_{rank_idx:03d}",
                rank=rank_idx,
                **item
            )
        )

    return PredictResponse(
        status="success",
        count=len(formatted_predictions),
        predictions=formatted_predictions
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)