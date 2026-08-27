from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any

class GeoJSONPoint(BaseModel):
    type: str = "Point"
    coordinates: List[float] = Field(..., description="[longitude, latitude]")

class LocationBase(BaseModel):
    location_id: str
    region: str
    location_metadata: Optional[Dict[str, Any]] = None

class LocationResponse(LocationBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    geometry: GeoJSONPoint
    risk_score: Optional[float] = None
    risk_level: Optional[str] = None
    predicted_window: Optional[str] = None