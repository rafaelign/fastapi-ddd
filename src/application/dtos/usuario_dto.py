from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, validator

from src.domain.entities.usuario import PerfilUsuario

class UsuarioBase(BaseModel):
    email: EmailStr
    nome: str = Field(..., min_length=2, max_length=100)

class UsuarioCreate(UsuarioBase):
    senha: str = Field(..., min_length=8)
    perfil: PerfilUsuario = PerfilUsuario.USUARIO

class UsuarioUpdate(BaseModel):
    email: Optional[EmailStr] = None
    nome: Optional[str] = Field(None, min_length=2, max_length=100)
    senha: Optional[str] = Field(None, min_length=8)
    perfil: Optional[PerfilUsuario] = None
    ativo: Optional[bool] = None

class UsuarioResponse(UsuarioBase):
    id: UUID
    perfil: PerfilUsuario
    ativo: bool
    data_criacao: datetime
    data_atualizacao: datetime
    ultimo_login: Optional[datetime] = None

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    email: EmailStr
    senha: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioResponse