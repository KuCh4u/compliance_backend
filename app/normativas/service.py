from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Estandar
from .schemas import EstandarCreate

async def create_estandar(db: AsyncSession, estandar: EstandarCreate) -> Estandar:
    nuevo_estandar = Estandar(
        nombre_estandar=estandar.nombre_estandar,
        descripcion=estandar.descripcion
    )

    db.add(nuevo_estandar)
    await db.commit()
    await db.refresh(nuevo_estandar)
    return nuevo_estandar

async def create_control():
    print("funca")