from motor.motor_asyncio import AsyncIOMotorClient
import certifi
from app.config import settings

class DataBase:
    client: AsyncIOMotorClient = None

db = DataBase()

async def connect_to_mongo():
    # Pass tlsCAFile using certifi to resolve SSL handshake errors
    db.client = AsyncIOMotorClient(
        settings.mongodb_connection_string,
        tlsCAFile=certifi.where()
    )
    print("Connected to MongoDB database.")

async def close_mongo_connection():
    if db.client:
        db.client.close()
        print("Closed MongoDB connection.")

def get_database():
    return db.client[settings.mongodb_db_name]