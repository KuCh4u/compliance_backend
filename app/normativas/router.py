from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from .schemas import EstandarCreate, EstandarResponse
from .service import create_estandar, create_control

router = APIRouter(prefix="/estandares", tags=["Estandares"])

@router.post("/", response_model=EstandarResponse)
async def crear_estandar(
    estandar: EstandarCreate,
    db: AsyncSession = Depends(get_db)
):
    print('estandar', estandar)
    # await create_estandar(db, estandar)
    # await create_control()
    return True