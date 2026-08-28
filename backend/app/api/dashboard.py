from fastapi import APIRouter, Depends
from app.schemas.dashboard import DashboardSummaryResponse
from app.auth.dependencies import get_current_user
from app.schemas.auth import TokenData
from app.db.mongo import get_database

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary", response_model=DashboardSummaryResponse)
async def get_dashboard_summary(current_user: TokenData = Depends(get_current_user)):
    db = get_database()

    # Query live metrics from MongoDB collections
    total_complaints = await db.complaints.count_documents({})
    high_risk_zones = await db.locations.count_documents({"risk_level": {"$in": ["HIGH", "CRITICAL"]}})
    active_alerts = await db.alerts.count_documents({"status": {"$in": ["NEW", "ACTIVE"]}})
    at_risk_atms = await db.locations.count_documents({"risk_score": {"$gte": 0.50}})

    # Count breakdown by risk level
    critical_count = await db.locations.count_documents({"risk_level": "CRITICAL"})
    high_count = await db.locations.count_documents({"risk_level": "HIGH"})
    medium_count = await db.locations.count_documents({"risk_level": "MEDIUM"})
    low_count = await db.locations.count_documents({"risk_level": "LOW"})

    return {
        "totalComplaints": total_complaints,
        "highRiskZones": high_risk_zones,
        "activeAlerts": active_alerts,
        "atRiskAtms": at_risk_atms,
        "risk_level_breakdown": {
            "CRITICAL": critical_count,
            "HIGH": high_count,
            "MEDIUM": medium_count,
            "LOW": low_count
        }
    }