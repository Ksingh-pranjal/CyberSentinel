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
    total_predictions = await db.predictions.count_documents({})
    high_risk_locations = await db.locations.count_documents({"risk_level": {"$in": ["HIGH", "CRITICAL"]}})
    active_alerts = await db.alerts.count_documents({"status": "ACTIVE"})
    acknowledged_alerts = await db.alerts.count_documents({"status": "ACKNOWLEDGED"})

    # Count breakdown by risk level
    critical_count = await db.locations.count_documents({"risk_level": "CRITICAL"})
    high_count = await db.locations.count_documents({"risk_level": "HIGH"})
    medium_count = await db.locations.count_documents({"risk_level": "MEDIUM"})
    low_count = await db.locations.count_documents({"risk_level": "LOW"})

    return {
        "total_predictions": total_predictions,
        "high_risk_locations": high_risk_locations,
        "active_alerts": active_alerts,
        "acknowledged_alerts": acknowledged_alerts,
        "risk_level_breakdown": {
            "CRITICAL": critical_count,
            "HIGH": high_count,
            "MEDIUM": medium_count,
            "LOW": low_count
        }
    }