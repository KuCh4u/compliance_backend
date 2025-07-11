from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models import Estandar
from .schemas import EstandarCreate, EstandarResumenResponse
from fastapi import UploadFile, HTTPException
import pandas as pd
from io import BytesIO
from app.models import Control

async def create_estandar(db: AsyncSession, estandar: EstandarCreate) -> Estandar:
    nuevo_estandar = Estandar(
        nombre_estandar=estandar.nombre_estandar,
        descripcion=estandar.descripcion
    )

    db.add(nuevo_estandar)
    await db.commit()
    await db.refresh(nuevo_estandar)
    return nuevo_estandar

async def create_control(file: UploadFile, db: AsyncSession, estandar_id: int):
    contents = await file.read()

    df = pd.read_excel(BytesIO(contents))
    df = df.fillna('')

    columnas_esperadas = [
        "Título", "Nombre del Título", "Artículo", "Nombre del Artículo",
        "Categoría Ciberseguridad (RoMax)", "Ámbito de Aplicación",
        "Requisito Legal", "Descripción Detallada"
    ]

    if not all(col in df.columns for col in columnas_esperadas):
        raise HTTPException(status_code=400, detail="El Excel no contiene todas las columnas requeridas.")
    
    for _, row in df.iterrows():
        control = Control(
            id_estandar=estandar_id,
            nombre_control=row["Nombre del Artículo"],
            funcion=row["Título"],
            categoria=row["Categoría Ciberseguridad (RoMax)"],
            descripcion_categoria=row["Nombre del Título"],
            subcategoria=row["Artículo"],
            escala_riesgo=row["Ámbito de Aplicación"],
            ejemplo_implementación=row["Descripción Detallada"],
            requisito_legal=row["Requisito Legal"]
        )
        db.add(control)

    await db.commit()

async def get_all_estandares_resumen(db: AsyncSession) -> list[EstandarResumenResponse]:
    stmt = (
        select(
            Estandar.id,
            Estandar.nombre_estandar,
            Estandar.descripcion,
            func.count(Control.id).label("cantidad_controles")
        )
        .outerjoin(Control, Control.id_estandar == Estandar.id)
        .group_by(Estandar.id)
    )

    result = await db.execute(stmt)
    rows = result.all()

    return [
        EstandarResumenResponse(
            id=row.id,
            nombre_estandar=row.nombre_estandar,
            descripcion=row.descripcion,
            cantidad_controles=row.cantidad_controles
        )
        for row in rows
    ]