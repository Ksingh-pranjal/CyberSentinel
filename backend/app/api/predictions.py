from fastapi import APIRouter
from app.db.mongo import get_database

router = APIRouter(prefix="/predictions", tags=["Predictions"])

@router.get("/")
async def get_predictions():
    db = get_database()
    predictions = await db.predictions.find({}, {"_id": 0}).to_list(length=100)
    return {"status": "success", "count": len(predictions), "data": predictions}