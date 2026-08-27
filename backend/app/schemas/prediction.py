from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class PredictionBase(BaseModel):
    location_id: str
    risk_score: float = Field(..., ge=0.0, le=1.0, description="Risk probability score between 0.0 and 1.0")
    risk_level: str  # LOW, MEDIUM, HIGH, CRITICAL
    predicted_window: str
    model_version: str = "v1.0"

class PredictionCreate(PredictionBase):
    pass

class PredictionResponse(PredictionBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)