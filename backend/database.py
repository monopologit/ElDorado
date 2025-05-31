from pymongo import MongoClient, IndexModel, ASCENDING, DESCENDING, TEXT
import os
from typing import Optional

# Configuración simple para MongoDB local
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB", "vagonetas_db")

# Cliente de MongoDB
client: Optional[MongoClient] = None
db = None

def connect_to_mongo():
    """Establece la conexión con MongoDB local"""
    global client, db
    if client is None:
        try:
            client = MongoClient(MONGO_URI)
            db = client[DB_NAME]
            
            # Crear índices básicos
            db.vagonetas.create_indexes([
                IndexModel([("numero", ASCENDING)]),
                IndexModel([("timestamp", DESCENDING)]),
                IndexModel([("evento", ASCENDING)])
            ])
            print("✅ Conexión a MongoDB establecida")
        except Exception as e:
            print(f"❌ Error conectando a MongoDB: {str(e)}")
            raise e

def close_mongo_connection():
    """Cierra la conexión con MongoDB"""
    global client
    if client:
        client.close()
        client = None
        db = None

def get_database():
    """Obtiene la base de datos, estableciendo la conexión si es necesario"""
    global db
    if db is None:
        connect_to_mongo()
    return db

def get_vagonetas_collection():
    """Obtiene la colección de vagonetas"""
    database = get_database()
    return database.vagonetas
