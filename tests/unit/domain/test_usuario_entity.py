import pytest
from datetime import datetime
from uuid import UUID

from src.domain.entities.usuario import Usuario, PerfilUsuario
from src.domain.exceptions.domain_exceptions import DomainValidationError

def test_criar_usuario_valido():
    # Arrange & Act
    usuario = Usuario(
        email="usuario@exemplo.com",
        senha_hash="hashed_password",
        nome="Usuário Teste"
    )
    
    # Assert
    assert isinstance(usuario.id, UUID)
    assert usuario.email == "usuario@exemplo.com"
    assert usuario.senha_hash == "hashed_password"
    assert usuario.nome == "Usuário Teste"
    assert usuario.perfil == PerfilUsuario.USUARIO
    assert usuario.ativo is True
    assert isinstance(usuario.data_criacao, datetime)
    assert isinstance(usuario.data_atualizacao, datetime)
    assert usuario.ultimo_login is None

def test_criar_usuario_com_perfil_admin():
    # Arrange & Act
    usuario = Usuario(
        email="admin@exemplo.com",
        senha_hash="hashed_password",
        nome="Admin Teste",
        perfil=PerfilUsuario.ADMIN
    )
    
    # Assert
    assert usuario.perfil == PerfilUsuario.ADMIN

def test_criar_usuario_email_invalido():
    # Arrange & Act & Assert
    with pytest.raises(DomainValidationError) as excinfo:
        Usuario(
            email="emailinvalido",
            senha_hash="hashed_password",
            nome="Usuário Teste"
        )
    
    assert "Email inválido" in str(excinfo.value)

def test_criar_usuario_nome_vazio():
    # Arrange & Act & Assert
    with pytest.raises(DomainValidationError) as excinfo:
        Usuario(
            email="usuario@exemplo.com",
            senha_hash="hashed_password",
            nome=""
        )
    
    assert "O nome não pode ser vazio" in str(excinfo.value)

def test_desativar_usuario():
    # Arrange
    usuario = Usuario(
        email="usuario@exemplo.com",
        senha_hash="hashed_password",
        nome="Usuário Teste"
    )
    
    # Act
    usuario.desativar()
    
    # Assert
    assert usuario.ativo is False

def test_ativar_usuario():
    # Arrange
    usuario = Usuario(
        email="usuario@exemplo.com",
        senha_hash="hashed_password",
        nome="Usuário Teste",
        ativo=False
    )
    
    # Act
    usuario.ativar()
    
    # Assert
    assert usuario.ativo is True

def test_registrar_login():
    # Arrange
    usuario = Usuario(
        email="usuario@exemplo.com",
        senha_hash="hashed_password",
        nome="Usuário Teste"
    )
    
    # Act
    usuario.registrar_login()
    
    # Assert
    assert usuario.ultimo_login is not None
    assert isinstance(usuario.ultimo_login, datetime)