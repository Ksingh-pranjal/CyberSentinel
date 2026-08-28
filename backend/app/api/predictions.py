from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from app.db.mongo import get_database
from app.schemas.prediction import PredictionResponse
from app.auth.dependencies import get_current_user
from app.schemas.auth import TokenData

router = APIRouter(prefix="/predictions", tags=["Predictions"])

@router.get("/", response_model=List[PredictionResponse])
async def get_predictions(
    region: Optional[str] = Query(default=None, description="Filter by geographic region"),
    crime_category: Optional[str] = Query(default=None, description="Filter by crime category"),
    predicted_window: Optional[str] = Query(default=None, description="Filter by forecast time window"),
    risk_level: Optional[str] = Query(default=None, description="Filter by risk severity (LOW, MEDIUM, HIGH, CRITICAL)"),
    current_user: TokenData = Depends(get_current_user)
):
    db = get_database()
    
    # 1. Build MongoDB match query
    query = {}
    if region:
        query["region"] = region
    if crime_category:
        query["crime_category"] = crime_category
    if predicted_window:
        query["predicted_window"] = predicted_window
    if risk_level:
        query["risk_level"] = risk_level.upper()

    # 2. Fetch predictions
    predictions = await db.predictions.find(query, {"_id": 0}).to_list(length=200)

    # 3. Enrich prediction data with location coordinates and metadata if missing
    locations_cache = {}
    enriched_predictions = []
    
    for p in predictions:
        loc_id = p.get("location_id")
        if loc_id and (p.get("latitude") is None or p.get("longitude") is None or not p.get("location_name")):
            if loc_id not in locations_cache:
                loc_doc = await db.locations.find_one({"location_id": loc_id}, {"_id": 0})
                locations_cache[loc_id] = loc_doc or {}
            
            loc_data = locations_cache[loc_id]
            if loc_data:
                if not p.get("location_name"):
                    p["location_name"] = loc_data.get("location_name", loc_id)
                if not p.get("region") and loc_data.get("region"):
                    p["region"] = loc_data.get("region")
                
                geom = loc_data.get("geometry", {})
                coords = geom.get("coordinates", [])
                if len(coords) == 2:
                    # GeoJSON is [longitude, latitude]
                    if p.get("longitude") is None:
                        p["longitude"] = coords[0]
                    if p.get("latitude") is None:
                        p["latitude"] = coords[1]
                        
        enriched_predictions.append(PredictionResponse.model_validate(p))

    return enriched_predictions

@router.get("/{prediction_id}", response_model=PredictionResponse)
async def get_prediction_by_id(
    prediction_id: str,
    current_user: TokenData = Depends(get_current_user)
):
    db = get_database()
    
    # 1. Fetch prediction by ID
    prediction = await db.predictions.find_one({"id": prediction_id}, {"_id": 0})
    if not prediction:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prediction with ID '{prediction_id}' was not found"
        )

    # 2. Enrich with location data if missing
    loc_id = prediction.get("location_id")
    if loc_id and (prediction.get("latitude") is None or prediction.get("longitude") is None or not prediction.get("location_name")):
        loc_data = await db.locations.find_one({"location_id": loc_id}, {"_id": 0})
        if loc_data:
            if not prediction.get("location_name"):
                prediction["location_name"] = loc_data.get("location_name", loc_id)
            if not prediction.get("region") and loc_data.get("region"):
                prediction["region"] = loc_data.get("region")
            geom = loc_data.get("geometry", {})
            coords = geom.get("coordinates", [])
            if len(coords) == 2:
                if prediction.get("longitude") is None:
                    prediction["longitude"] = coords[0]
                if prediction.get("latitude") is None:
                    prediction["latitude"] = coords[1]

    return PredictionResponse.model_validate(prediction)