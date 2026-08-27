from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timezone
from app.schemas.alert import AlertResponse, AlertAcknowledge
from app.auth.dependencies import get_current_user
from app.schemas.auth import TokenData

router = APIRouter(prefix="/alerts", tags=["Alerts"])

MOCK_ALERTS = [
    {
        "id": "alt_001",
        "prediction_id": "pred_101",
        "severity": "CRITICAL",
        "recipient_role": "LEA Officer",
        "status": "ACTIVE",
        "created_at": datetime.now(timezone.utc),
        "acknowledged_at": None
    }
]

@router.get("", response_model=List[AlertResponse])
def list_alerts(
    status: Optional[str] = Query(None, description="Filter by ACTIVE or ACKNOWLEDGED"),
    current_user: TokenData = Depends(get_current_user)
):
    if status:
        return [a for a in MOCK_ALERTS if a["status"] == status.upper()]
    return MOCK_ALERTS

@router.post("/{id}/acknowledge", response_model=AlertResponse)
def acknowledge_alert(
    id: str,
    payload: AlertAcknowledge,
    current_user: TokenData = Depends(get_current_user)
):
    for alert in MOCK_ALERTS:
        if alert["id"] == id:
            alert["status"] = "ACKNOWLEDGED"
            alert["acknowledged_at"] = datetime.now(timezone.utc)
            return alert
    raise HTTPException(status_code=404, detail="Alert not found")