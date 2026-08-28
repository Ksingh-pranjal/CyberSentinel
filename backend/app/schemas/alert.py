from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime, timezone

class AlertBase(BaseModel):
    prediction_id: str
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    recipient_role: Optional[str] = "LEA Officer"  # LEA Officer, Bank/FI, I4C Analyst, Admin
    status: str = "NEW"  # NEW, ACKNOWLEDGED

class AlertCreate(AlertBase):
    id: Optional[str] = None

class AlertAcknowledge(BaseModel):
    acknowledged_by: Optional[str] = None
    notes: Optional[str] = None

class AlertResponse(AlertBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    acknowledged_at: Optional[datetime] = None