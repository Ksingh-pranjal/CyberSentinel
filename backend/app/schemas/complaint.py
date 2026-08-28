from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime, timezone

class ComplaintBase(BaseModel):
    complaint_id: str
    crime_category: str
    region: str
    account_number: Optional[str] = None
    amount: float = Field(..., ge=0.0)

class ComplaintCreate(ComplaintBase):
    timestamp: Optional[datetime] = None

class ComplaintResponse(ComplaintBase):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
