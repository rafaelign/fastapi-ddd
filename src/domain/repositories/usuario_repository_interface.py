from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.entities.usuario import Usuario

class UsuarioRepositoryInterface(ABC):
    """Interface para o repositório de usuários seguindo o padrão Repository do DDD."""
    
    @abstractmethod
    async def criar(self, usuario: Usuario) -> Usuario:
        """Cria um novo usuário."""
        pass
    
    @abstractmethod
    async def atualizar(self, usuario: Usuario) -> Usuario:
        """Atualiza um usuário existente."""
        pass
    
    @abstractmethod
    async def obter_por_id(self, usuario_id: UUID) -> Optional[Usuario]:
        """Obtém um usuário pelo ID."""
        pass
    
    @abstractmethod
    async def obter_por_email(self, email: str) -> Optional[Usuario]:
        """Obtém um usuário pelo email."""
        pass
    
    @abstractmethod
    async def listar(self, skip: int = 0, limit: int = 100) -> List[Usuario]:
        """Lista usuários com paginação."""
        pass
    
    @abstractmethod
    async def remover(self, usuario_id: UUID) -> bool:
        """Remove um usuário pelo ID."""
        pass