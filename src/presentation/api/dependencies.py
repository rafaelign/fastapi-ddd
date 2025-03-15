from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db
from src.domain.entities.usuario import Usuario, PerfilUsuario
from src.domain.exceptions.domain_exceptions import AuthenticationError, AuthorizationError
from src.domain.repositories.usuario_repository_interface import UsuarioRepositoryInterface
from src.infrastructure.auth.jwt_handler import decode_token
from src.infrastructure.database.repositories.usuario_repository import UsuarioRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_usuario_repository(db: AsyncSession = Depends(get_db)) -> UsuarioRepositoryInterface:
    return UsuarioRepository(db)

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    usuario_repository: UsuarioRepositoryInterface = Depends(get_usuario_repository)
) -> Usuario:
    credentials_exception = AuthenticationError("Credenciais inválidas")
    
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    
    usuario_id = payload.get("sub")
    if usuario_id is None:
        raise credentials_exception
    
    usuario = await usuario_repository.obter_por_id(usuario_id)
    if usuario is None:
        raise credentials_exception
    
    if not usuario.ativo:
        raise AuthenticationError("Usuário desativado")
    
    return usuario

async def get_current_admin_user(
    current_user: Annotated[Usuario, Depends(get_current_user)]
) -> Usuario:
    if current_user.perfil != PerfilUsuario.ADMIN:
        raise AuthorizationError("Acesso apenas para administradores")
    return current_user