from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from src.domain.exceptions.domain_exceptions import DomainValidationError

class PerfilUsuario(str, Enum):
    ADMIN = "admin"
    USUARIO = "usuario"

@dataclass
class Usuario:
    email: str
    senha_hash: str
    nome: str
    perfil: PerfilUsuario = PerfilUsuario.USUARIO
    id: UUID = None
    ativo: bool = True
    data_criacao: datetime = None
    data_atualizacao: datetime = None
    ultimo_login: Optional[datetime] = None

    def __post_init__(self):
        # Gerar ID se não fornecido
        if self.id is None:
            self.id = uuid4()
        
        # Definir datas se não fornecidas
        if self.data_criacao is None:
            self.data_criacao = datetime.utcnow()
        
        self.data_atualizacao = datetime.utcnow()
            
        # Validações
        self._validar()
    
    def _validar(self) -> None:
        if not self.email or len(self.email.strip()) == 0:
            raise DomainValidationError("O email não pode ser vazio")
        
        if not "@" in self.email:
            raise DomainValidationError("Email inválido")
        
        if not self.nome or len(self.nome.strip()) == 0:
            raise DomainValidationError("O nome não pode ser vazio")
    
    def desativar(self) -> None:
        self.ativo = False
        self.data_atualizacao = datetime.utcnow()
    
    def ativar(self) -> None:
        self.ativo = True
        self.data_atualizacao = datetime.utcnow()
    
    def registrar_login(self) -> None:
        self.ultimo_login = datetime.utcnow()