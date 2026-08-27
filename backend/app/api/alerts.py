from fastapi import APIRouter
from app.db.mongo import get_database

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.get("/")
async def get_alerts():
    db = get_database()
    alerts = await db.alerts.find({}, {"_id": 0}).to_list(length=100)
    return {"status": "success", "count": len(alerts), "data": alerts}