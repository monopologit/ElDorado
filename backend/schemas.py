from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class VagonetaBase(BaseModel):
    numero: Optional[str] = None
    imagen_path: str
    timestamp: datetime
    tunel: Optional[str] = None
    evento: str  # 'ingreso' o 'egreso'
    modelo_ladrillo: Optional[str] = None  # modelo detectado o ingresado
    merma: Optional[float] = None  # porcentaje de merma/fisuración
    
    # Puedes agregar más campos según necesidades futuras

class VagonetaCreate(VagonetaBase):
    pass

class VagonetaInDB(VagonetaBase):
    id: str = Field(..., alias="_id")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
