from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

class CaseTimelineItem(BaseModel):
    time: str
    event: str
    location: str

class CaseBase(BaseModel):
    status: str = "ACTIVE"  # ACTIVE, PENDING, CLOSED
    summary: str
    risk_level: str  # LOW, MEDIUM, HIGH, CRITICAL
    complaints: List[str] = Field(default_factory=list)
    hotspot_ids: List[str] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)
    timeline: List[CaseTimelineItem] = Field(default_factory=list)

class CaseCreate(CaseBase):
    id: str

class CaseNoteCreate(BaseModel):
    note: str

class CaseResponse(CaseBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
