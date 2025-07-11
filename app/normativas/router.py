from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from .schemas import EstandarCreate, EstandarResponse, EstandarResumenResponse
from .service import create_estandar, create_control, get_all_estandares_resumen
from typing import Optional, List

router = APIRouter(prefix="/estandares", tags=["Estandares"])

@router.post("/", response_model=EstandarResponse)
async def crear_estandar(
    nombre_estandar: str = Form(...),
    descripcion: Optional[str] = Form(''),
    archivo: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    estandar = EstandarCreate(nombre_estandar=nombre_estandar, descripcion=descripcion)
    nuevo_estandar = await create_estandar(db, estandar)
    await create_control(archivo, db, nuevo_estandar.id)
    return nuevo_estandar

@router.get("/", response_model=List[EstandarResumenResponse])
async def get_all_estandares(db: AsyncSession = Depends(get_db)):
    return await get_all_estandares_resumen(db)