from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EstandarCreate(BaseModel):
    nombre_estandar: str
    descripcion: Optional[str] = None

class EstandarResponse(BaseModel):
    id: int
    nombre_estandar: str
    descripcion: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class EstandarResumenResponse(BaseModel):
    nombre_estandar: str
    descripcion: Optional[str]
    cantidad_controles: int

    class Config:
        orm_mode = True