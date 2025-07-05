from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from .schemas import LoginRequest, TokenResponse, CreateUser, UserOut
from .service import login_user, crear_usuario
from app.utils.recaptcha import verify_recaptcha

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
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/register", response_model=UserOut)
async def register_usuario(usuario: CreateUser, db: AsyncSession = Depends(get_db)):
    try:
        nuevo_usuario = await crear_usuario(usuario, db)
        return nuevo_usuario
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))