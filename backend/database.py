from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB", "vagonetas_db")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

# Colección para los registros de vagonetas
vagonetas_collection = db["vagonetas"]
