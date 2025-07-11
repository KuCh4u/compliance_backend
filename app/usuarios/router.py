from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from .schemas import LoginRequest, TokenResponse, CreateUser, UserOut, UsersTypes
from .service import login_user, crear_usuario, get_all_users_types
from app.utils.recaptcha import verify_recaptcha
from typing import List

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    try:
        # if not await verify_recaptcha(request.recaptcha_token) and False:
        #     raise HTTPException(status_code=400, detail="reCAPTCHA inválido")
        token = await login_user(db, request.email, request.password)
        # if not token or token == False:
        #     raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")
        return token
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/register", response_model=UserOut)
async def register_usuario(usuario: CreateUser, db: AsyncSession = Depends(get_db)):
    try:
        nuevo_usuario = await crear_usuario(usuario, db)
        return nuevo_usuario
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/user-types", response_model=List[UsersTypes])
async def get_all_user_types(db: AsyncSession = Depends(get_db)):
    try:
        return await get_all_users_types(db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))