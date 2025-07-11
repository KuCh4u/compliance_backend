from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from .database import Base, engine, SessionLocal
from . import models
from app.usuarios.router import router as usuarios_router
from app.normativas.router import router as normativas_router
from app.clientes.router import router as clientes_router

app = FastAPI()

app.include_router(usuarios_router)
app.include_router(normativas_router)
app.include_router(clientes_router)

origins = [
    "http://localhost:5173",
    "https://compliance-alpha.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],              # Puedes usar ["*"] para desarrollo
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def read_root():
    return {"message": "API Compliance lista"}
