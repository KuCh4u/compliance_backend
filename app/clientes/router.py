# routers/cliente.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from .schema import ClienteCreate, ClienteResponse
from .service import create_cliente, get_all_clientes
from typing import List

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.post("/register", response_model=ClienteResponse)
async def crear_cliente(
    cliente: ClienteCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await create_cliente(db, cliente)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[ClienteResponse])
async def listar_clientes(db: AsyncSession = Depends(get_db)):
    return await get_all_clientes(db)