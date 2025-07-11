# schemas/cliente.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ClienteCreate(BaseModel):
    identificador_cliente: str
    nombre_cliente: str
    tipo_cliente: str
    tamano: Optional[str] = None
    rubro_id: Optional[int] = None
    region_id: Optional[int] = None

class RubroOut(BaseModel):
    id: int
    descripcion: str

    class Config:
        orm_mode = True

class RegionOut(BaseModel):
    id: int
    descripcion: str

    class Config:
        orm_mode = True

class ClienteResponse(BaseModel):
    id: int
    identificador_cliente: str
    nombre_cliente: str
    tipo_cliente: str
    tamano: Optional[str]
    rubro: Optional[RubroOut]      # ✅ relación anidada
    region: Optional[RegionOut]    # ✅ relación anidada
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True