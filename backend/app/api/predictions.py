from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timezone
from app.schemas.prediction import PredictionResponse, PredictionCreate
from app.auth.dependencies import get_current_user, require_role
from app.schemas.auth import TokenData

router = APIRouter(prefix="/predictions", tags=["Predictions"])

MOCK_PREDICTIONS = [
    {
        "id": "pred_101",
        "location_id": "loc_001",
        "risk_score": 0.85,
        "risk_level": "CRITICAL",
        "predicted_window": "2026-08-27 00:00-06:00",
        "model_version": "v1.0",
        "created_at": datetime.now(timezone.utc)
    },
    {
        "id": "pred_102",
        "location_id": "loc_002",
        "risk_score": 0.65,
        "risk_level": "HIGH",
        "predicted_window": "2026-08-27 06:00-12:00",
        "model_version": "v1.0",
        "created_at": datetime.now(timezone.utc)
    }
]

@router.get("", response_model=List[PredictionResponse])
def list_predictions(
    risk_level: Optional[str] = Query(None, description="Filter by risk level"),
    current_user: TokenData = Depends(get_current_user)
):
    if risk_level:
        return [p for p in MOCK_PREDICTIONS if p["risk_level"] == risk_level.upper()]
    return MOCK_PREDICTIONS

@router.get("/{id}", response_model=PredictionResponse)
def get_prediction(id: str, current_user: TokenData = Depends(get_current_user)):
    for p in MOCK_PREDICTIONS:
        if p["id"] == id:
            return p
    raise HTTPException(status_code=404, detail="Prediction not found")

@router.post("/run", response_model=PredictionResponse)
def run_mock_prediction(
    payload: PredictionCreate,
    current_user: TokenData = Depends(require_role(["Admin", "LEA Officer"]))
):
    new_pred = {
        "id": f"pred_{len(MOCK_PREDICTIONS) + 101}",
        **payload.model_dump(),
        "created_at": datetime.now(timezone.utc)
    }
    MOCK_PREDICTIONS.append(new_pred)
    return new_pred