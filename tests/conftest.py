import asyncio
from datetime import datetime
from typing import AsyncGenerator
from uuid import uuid4

import pytest
import pytest_asyncio
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from src.config.database import Base, get_db
from src.domain.entities.usuario import Usuario, PerfilUsuario
from src.infrastructure.database.models.usuario_model import UsuarioModel
from src.main import app

# SQLite em memória para testes
TEST_SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="session")
def event_loop():
    """Sobrescreve o event_loop pytest-asyncio para ter escopo de sessão"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session")
async def setup_db():
    """Configura o banco de dados de teste e retorna um motor de banco de dados."""
    engine = create_async_engine(
        TEST_SQLALCHEMY_DATABASE_URL,
        poolclass=NullPool,
    )
    
    # Criar tabelas
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine