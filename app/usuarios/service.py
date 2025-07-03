from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session, selectinload  # Solo si haces testing sin async

from app.models import Usuario
from .auth import verify_password, create_access_token, hash_password
from . import schemas

# Crear un nuevo usuario
async def crear_usuario(usuario_data: schemas.CreateUser, db: AsyncSession) -> Usuario:
    hashed_pw = hash_password(usuario_data.password)
    nuevo_usuario = Usuario(
        nombre=usuario_data.nombre,
        email=usuario_data.email,
        password=hashed_pw,
        tipo_usuario_id=usuario_data.tipo_usuario_id,
        cliente_id=usuario_data.cliente_id
    )
    db.add(nuevo_usuario)
    await db.commit()
    await db.refresh(nuevo_usuario)
    return nuevo_usuario

# Autenticación de usuario (sin token)
async def authenticate_user(db: AsyncSession, email: str, password: str):
    result = await db.execute(
        select(Usuario)
        .options(selectinload(Usuario.tipo_usuario))
        .where(Usuario.email == email, Usuario.is_active == True)
    )
    user = result.scalars().first()
    if not user or not verify_password(password, user.password):
        return None
    return user

# Login de usuario (con retorno de token JWT)
async def login_user(db: AsyncSession, email: str, password: str):
    user = await authenticate_user(db, email, password)
    print('USER VALIDATION', not user, user.is_active, user.is_deleted)
    if not user or user.is_active == False or user.is_deleted == True:
        return None
    
    token = create_access_token(data={"email": user.email, "id": user.id, "nombre": user.nombre, "client_id": user.cliente_id})

    return {"access_token": token, "token_type": "bearer"}
