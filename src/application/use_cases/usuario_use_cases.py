from datetime import datetime, timedelta
from typing import List, Optional
from uuid import UUID

import bcrypt

from src.application.dtos.usuario_dto import (
    UsuarioCreate, 
    UsuarioUpdate, 
    UsuarioResponse, 
    TokenResponse
)
from src.config.settings import get_settings
from src.domain.entities.usuario import Usuario
from src.domain.exceptions.domain_exceptions import (
    DomainValidationError, 
    EntityNotFoundError, 
    AuthenticationError
)
from src.domain.repositories.usuario_repository_interface import UsuarioRepositoryInterface
from src.infrastructure.auth.jwt_handler import create_access_token

settings = get_settings()

class UsuarioUseCases:
    def __init__(self, usuario_repository: UsuarioRepositoryInterface):
        self.usuario_repository = usuario_repository
    
    async def criar_usuario(self, usuario_create: UsuarioCreate) -> UsuarioResponse:
        # Verificar se já existe usuário com este email
        usuario_existente = await self.usuario_repository.obter_por_email(usuario_create.email)
        if usuario_existente:
            raise DomainValidationError(f"Já existe um usuário com o email {usuario_create.email}")
        
        # Hash da senha
        senha_hash = self._gerar_hash_senha(usuario_create.senha)
        
        # Criar entidade de usuário
        usuario = Usuario(
            email=usuario_create.email,
            senha_hash=senha_hash,
            nome=usuario_create.nome,
            perfil=usuario_create.perfil
        )
        
        # Salvar no repositório
        usuario_criado = await self.usuario_repository.criar(usuario)
        
        # Retornar DTO de resposta
        return self._converter_para_dto(usuario_criado)
    
    async def atualizar_usuario(
        self, 
        usuario_id: UUID, 
        usuario_update: UsuarioUpdate
    ) -> UsuarioResponse:
        # Buscar usuário existente
        usuario = await self.usuario_repository.obter_por_id(usuario_id)
        if not usuario:
            raise EntityNotFoundError(f"Usuário com ID {usuario_id} não encontrado")
        
        # Atualizar campos
        if usuario_update.email is not None:
            # Verificar se o novo email já está em uso por outro usuário
            if usuario_update.email != usuario.email:
                usuario_existente = await self.usuario_repository.obter_por_email(usuario_update.email)
                if usuario_existente and usuario_existente.id != usuario_id:
                    raise DomainValidationError(f"Email {usuario_update.email} já está em uso")
            usuario.email = usuario_update.email
        
        if usuario_update.nome is not None:
            usuario.nome = usuario_update.nome
        
        if usuario_update.senha is not None:
            usuario.senha_hash = self._gerar_hash_senha(usuario_update.senha)
        
        if usuario_update.perfil is not None:
            usuario.perfil = usuario_update.perfil
        
        if usuario_update.ativo is not None:
            if usuario_update.ativo:
                usuario.ativar()
            else:
                usuario.desativar()
        
        # Atualizar data de modificação
        usuario.data_atualizacao = datetime.utcnow()
        
        # Salvar no repositório
        usuario_atualizado = await self.usuario_repository.atualizar(usuario)
        
        # Retornar DTO de resposta
        return self._converter_para_dto(usuario_atualizado)
    
    async def obter_usuario(self, usuario_id: UUID) -> UsuarioResponse:
        usuario = await self.usuario_repository.obter_por_id(usuario_id)
        if not usuario:
            raise EntityNotFoundError(f"Usuário com ID {usuario_id} não encontrado")
        
        return self._converter_para_dto(usuario)
    
    async def listar_usuarios(self, skip: int = 0, limit: int = 100) -> List[UsuarioResponse]:
        usuarios = await self.usuario_repository.listar(skip, limit)
        return [self._converter_para_dto(usuario) for usuario in usuarios]
    
    async def remover_usuario(self, usuario_id: UUID) -> bool:
        usuario = await self.usuario_repository.obter_por_id(usuario_id)
        if not usuario:
            raise EntityNotFoundError(f"Usuário com ID {usuario_id} não encontrado")
        
        return await self.usuario_repository.remover(usuario_id)
    
    async def autenticar_usuario(self, email: str, senha: str) -> TokenResponse:
        usuario = await self.usuario_repository.obter_por_email(email)
        if not usuario:
            raise AuthenticationError("Email ou senha inválidos")
        
        if not usuario.ativo:
            raise AuthenticationError("Usuário desativado")
        
        if not self._verificar_senha(senha, usuario.senha_hash):
            raise AuthenticationError("Email ou senha inválidos")
        
        # Registrar login
        usuario.registrar_login()
        await self.usuario_repository.atualizar(usuario)
        
        # Gerar token JWT
        token_data = {
            "sub": str(usuario.id),
            "email": usuario.email,
            "perfil": usuario.perfil
        }
        
        access_token = create_access_token(
            data=token_data,
            expires_delta=timedelta(minutes=settings.JWT_EXPIRES_MINUTES)
        )
        
        # Retornar resposta com token
        return TokenResponse(
            access_token=access_token,
            usuario=self._converter_para_dto(usuario)
        )
    
    def _gerar_hash_senha(self, senha: str) -> str:
        # Gerar salt e hash da senha
        senha_bytes = senha.encode('utf-8')
        salt = bcrypt.gensalt()
        senha_hash = bcrypt.hashpw(senha_bytes, salt)
        return senha_hash.decode('utf-8')
    
    def _verificar_senha(self, senha: str, senha_hash: str) -> bool:
        # Verificar senha
        senha_bytes = senha.encode('utf-8')
        senha_hash_bytes = senha_hash.encode('utf-8')
        return bcrypt.checkpw(senha_bytes, senha_hash_bytes)
    
    def _converter_para_dto(self, usuario: Usuario) -> UsuarioResponse:
        return UsuarioResponse(
            id=usuario.id,
            email=usuario.email,
            nome=usuario.nome,
            perfil=usuario.perfil,
            ativo=usuario.ativo,
            data_criacao=usuario.data_criacao,
            data_atualizacao=usuario.data_atualizacao,
            ultimo_login=usuario.ultimo_login
        )