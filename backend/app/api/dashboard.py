from fastapi import APIRouter, Depends
from app.schemas.dashboard import DashboardSummaryResponse
from app.auth.dependencies import get_current_user
from app.schemas.auth import TokenData

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary", response_model=DashboardSummaryResponse)
def get_dashboard_summary(current_user: TokenData = Depends(get_current_user)):
    return {
        "total_predictions": 128,
        "high_risk_locations": 14,
        "active_alerts": 5,
        "acknowledged_alerts": 23,
        "risk_level_breakdown": {
            "CRITICAL": 3,
            "HIGH": 11,
            "MEDIUM": 34,
            "LOW": 80
        }
    }