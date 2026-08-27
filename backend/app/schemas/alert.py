from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class AlertBase(BaseModel):
    prediction_id: str
    severity: str  # MEDIUM, HIGH, CRITICAL
    recipient_role: str  # LEA Officer, Bank/FI, Admin
    status: str = "ACTIVE"  # ACTIVE, ACKNOWLEDGED

class AlertCreate(AlertBase):
    pass

class AlertAcknowledge(BaseModel):
    acknowledged_by: str
    notes: Optional[str] = None

class AlertResponse(AlertBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    acknowledged_at: Optional[datetime] = None