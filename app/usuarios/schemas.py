from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: str
    password: str
    recaptcha_token: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class CreateUser(BaseModel):
    nombre: str
    email: EmailStr
    password: str
    tipo_usuario_id: int
    cliente_id: int | None = None

class UserOut(BaseModel):
    id: int
    nombre: str
    email: EmailStr