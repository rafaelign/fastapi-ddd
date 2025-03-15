from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.domain.entities.usuario import Usuario, PerfilUsuario
from src.domain.repositories.usuario_repository_interface import UsuarioRepositoryInterface
from src.infrastructure.database.models.usuario_model import UsuarioModel

class UsuarioRepository(UsuarioRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def criar(self, usuario: Usuario) -> Usuario:
        db_usuario = UsuarioModel(
            id=usuario.id,
            email=usuario.email,
            senha_hash=usuario.senha_hash,
            nome=usuario.nome,
            perfil=usuario.perfil,
            ativo=usuario.ativo,
            data_criacao=usuario.data_criacao,
            data_atualizacao=usuario.data_atualizacao,
            ultimo_login=usuario.ultimo_login
        )
        
        self.session.add(db_usuario)
        await self.session.commit()
        await self.session.refresh(db_usuario)
        
        return self._mapear_para_entidade(db_usuario)
    
    async def atualizar(self, usuario: Usuario) -> Usuario:
        stmt = select(UsuarioModel).where(UsuarioModel.id == usuario.id)
        result = await self.session.execute(stmt)
        db_usuario = result.scalar_one_or_none()
        
        if db_usuario:
            db_usuario.email = usuario.email
            db_usuario.senha_hash = usuario.senha_hash
            db_usuario.nome = usuario.nome
            db_usuario.perfil = usuario.perfil
            db_usuario.ativo = usuario.ativo
            db_usuario.data_atualizacao = usuario.data_atualizacao
            db_usuario.ultimo_login = usuario.ultimo_login
            
            await self.session.commit()
            await self.session.refresh(db_usuario)
            
        return self._mapear_para_entidade(db_usuario) if db_usuario else None
    
    async def obter_por_id(self, usuario_id: UUID) -> Optional[Usuario]:
        stmt = select(UsuarioModel).where(UsuarioModel.id == usuario_id)
        result = await self.session.execute(stmt)
        db_usuario = result.scalar_one_or_none()
        
        return self._mapear_para_entidade(db_usuario) if db_usuario else None
    
    async def obter_por_email(self, email: str) -> Optional[Usuario]:
        stmt = select(UsuarioModel).where(UsuarioModel.email == email)
        result = await self.session.execute(stmt)
        db_usuario = result.scalar_one_or_none()
        
        return self._mapear_para_entidade(db_usuario) if db_usuario else None
    
    async def listar(self, skip: int = 0, limit: int = 100) -> List[Usuario]:
        stmt = select(UsuarioModel).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        db_usuarios = result.scalars().all()
        
        return [self._mapear_para_entidade(db_usuario) for db_usuario in db_usuarios]
    
    async def remover(self, usuario_id: UUID) -> bool:
        stmt = select(UsuarioModel).where(UsuarioModel.id == usuario_id)
        result = await self.session.execute(stmt)
        db_usuario = result.scalar_one_or_none()
        
        if db_usuario:
            await self.session.delete(db_usuario)
            await self.session.commit()
            return True
            
        return False
    
    def _mapear_para_entidade(self, model: UsuarioModel) -> Usuario:
        return Usuario(
            id=model.id,
            email=model.email,
            senha_hash=model.senha_hash,
            nome=model.nome,
            perfil=model.perfil,
            ativo=model.ativo,
            data_criacao=model.data_criacao,
            data_atualizacao=model.data_atualizacao,
            ultimo_login=model.ultimo_login
        )