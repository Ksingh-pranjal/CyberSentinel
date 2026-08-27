from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from app.schemas.location import LocationResponse
from app.auth.dependencies import get_current_user
from app.schemas.auth import TokenData

router = APIRouter(prefix="/locations", tags=["Locations / Heatmap"])

MOCK_LOCATIONS = [
    {
        "id": "loc_001",
        "location_id": "LOC_MUMBAI_01",
        "region": "West",
        "geometry": {"type": "Point", "coordinates": [72.8777, 19.0760]},
        "risk_score": 0.85,
        "risk_level": "CRITICAL",
        "predicted_window": "2026-08-27 00:00-06:00",
        "location_metadata": {"atm_id": "ATM_1092", "city": "Mumbai"}
    },
    {
        "id": "loc_002",
        "location_id": "LOC_DELHI_02",
        "region": "North",
        "geometry": {"type": "Point", "coordinates": [77.2090, 28.6139]},
        "risk_score": 0.65,
        "risk_level": "HIGH",
        "predicted_window": "2026-08-27 06:00-12:00",
        "location_metadata": {"atm_id": "ATM_2041", "city": "Delhi"}
    }
]

@router.get("", response_model=List[LocationResponse])
def get_heatmap_locations(
    risk_level: Optional[str] = Query(None, description="Filter map by risk level"),
    region: Optional[str] = Query(None, description="Filter map by region"),
    current_user: TokenData = Depends(get_current_user)
):
    filtered = MOCK_LOCATIONS
    if risk_level:
        filtered = [l for l in filtered if l.get("risk_level") == risk_level.upper()]
    if region:
        filtered = [l for l in filtered if l.get("region").lower() == region.lower()]
    return filtered