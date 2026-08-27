import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
from app.config import settings
import certifi
import hashlib

def get_password_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

async def seed():
    print("Connecting to MongoDB Atlas...")
    client = AsyncIOMotorClient(
        settings.mongodb_connection_string,
        tlsCAFile=certifi.where()
    )
    db = client[settings.mongodb_db_name]

    print("Cleaning existing collections...")
    await db.users.delete_many({})
    await db.locations.delete_many({})
    await db.predictions.delete_many({})
    await db.alerts.delete_many({})

    print("Seeding Users...")
    await db.users.insert_many([
        {
            "username": "officer@cybersentinel.gov",
            "password_hash": get_password_hash("officer123"),
            "role": "LEA Officer"
        },
        {
            "username": "admin@cybersentinel.gov",
            "password_hash": get_password_hash("admin123"),
            "role": "Admin"
        }
    ])

    print("Seeding Locations...")
    await db.locations.insert_many([
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
    ])

    print("Seeding Predictions...")
    await db.predictions.insert_many([
        {
            "id": "pred_101",
            "location_id": "loc_001",
            "risk_score": 0.85,
            "risk_level": "CRITICAL",
            "predicted_window": "2026-08-27 00:00-06:00",
            "model_version": "v1.0",
            "created_at": datetime.now(timezone.utc)
        },
        {
            "id": "pred_102",
            "location_id": "loc_002",
            "risk_score": 0.65,
            "risk_level": "HIGH",
            "predicted_window": "2026-08-27 06:00-12:00",
            "model_version": "v1.0",
            "created_at": datetime.now(timezone.utc)
        }
    ])

    print("Seeding Alerts...")
    await db.alerts.insert_many([
        {
            "id": "alt_001",
            "prediction_id": "pred_101",
            "severity": "CRITICAL",
            "recipient_role": "LEA Officer",
            "status": "ACTIVE",
            "created_at": datetime.now(timezone.utc),
            "acknowledged_at": None
        }
    ])

    print("MongoDB Atlas seeding completed successfully!")
    client.close()

if __name__ == "__main__":
    asyncio.run(seed())