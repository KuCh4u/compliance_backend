# services/cliente.py
from app.models import Cliente
from .schema import ClienteCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

async def create_cliente(db: AsyncSession, cliente: ClienteCreate) -> Cliente:
    nuevo_cliente = Cliente(**cliente.dict())
    db.add(nuevo_cliente)
    await db.commit()
    await db.refresh(nuevo_cliente)
    return nuevo_cliente

async def get_all_clientes(db: AsyncSession) -> list[Cliente]:
    result = await db.execute(
        select(Cliente)
        .options(
            selectinload(Cliente.rubro),
            selectinload(Cliente.region)
        )
    )
    return result.scalars().all()