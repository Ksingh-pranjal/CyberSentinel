from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
import certifi
from app.config import settings

class DataBase:
    client: Optional[AsyncIOMotorClient] = None

db = DataBase()

async def connect_to_mongo():
    # Pass tlsCAFile using certifi to resolve SSL handshake errors
    try:
        db.client = AsyncIOMotorClient(
            settings.mongodb_connection_string,
            tlsCAFile=certifi.where()
        )
        # Ping database to verify connection
        await db.client.admin.command('ping')
        print("Connected to MongoDB database.")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {str(e)}")
        raise e

async def close_mongo_connection():
    if db.client:
        db.client.close()
        print("Closed MongoDB connection.")

def get_database():
    if db.client is None:
        raise RuntimeError("Database client is not initialized. Ensure connect_to_mongo() has been called and succeeded.")
    return db.client[settings.mongodb_db_name]