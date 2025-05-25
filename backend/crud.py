from .database import vagonetas_collection
from .schemas import VagonetaCreate
from datetime import datetime

async def create_vagoneta_record(data: VagonetaCreate):
    doc = data.dict(by_alias=True)
    result = await vagonetas_collection.insert_one(doc)
    return str(result.inserted_id)

async def get_vagonetas_historial(skip: int = 0, limit: int = 50, numero: str = None, fecha: str = None):
    query = {}
    if numero:
        query["numero"] = numero
    if fecha:
        # Suponiendo que fecha es YYYY-MM-DD
        from datetime import datetime, timedelta
        start = datetime.strptime(fecha, "%Y-%m-%d")
        end = start + timedelta(days=1)
        query["timestamp"] = {"$gte": start, "$lt": end}
    cursor = vagonetas_collection.find(query).skip(skip).limit(limit)
    return [doc async for doc in cursor]
