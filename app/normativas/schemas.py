from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from fastapi import UploadFile

class EstandarCreate(BaseModel):
    nombre_estandar: str
    descripcion: Optional[str] = None
    archivo: UploadFile

class EstandarResponse(BaseModel):
    id: int
    nombre_estandar: str
    descripcion: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True