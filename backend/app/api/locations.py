from fastapi import APIRouter, HTTPException
from app.db.mongo import get_database

router = APIRouter(prefix="/locations", tags=["Locations"])

@router.get("/")
async def get_locations():
    db = get_database()
    locations = await db.locations.find({}, {"_id": 0}).to_list(length=100)
    return {"status": "success", "count": len(locations), "data": locations}

@router.get("/{location_id}")
async def get_location_by_id(location_id: str):
    db = get_database()
    location = await db.locations.find_one({"location_id": location_id}, {"_id": 0})
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return {"status": "success", "data": location}