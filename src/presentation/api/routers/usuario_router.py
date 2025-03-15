from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.application.dtos.usuario_dto import (
    UsuarioCreate,
    UsuarioResponse,
    UsuarioUpdate,
    LoginRequest,
    TokenResponse
)
from src.application.use_cases.usuario_use_cases import UsuarioUseCases
from src.domain.entities.usuario import Usuario
from src.domain.repositories.usuario_repository_interface import UsuarioRepositoryInterface
from src.presentation.api.dependencies import (
    get_usuario_repository,
    get_current_user,
    get_current_admin_user
)

router = APIRouter(tags=["Usuários"])

# Endpoint de criação de usuário (público)
@router.post(
    "/usuarios",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar um novo usuário"
)
async def criar_usuario(
    usuario_create: UsuarioCreate,
    usuario_repository: UsuarioRepositoryInterface = Depends(get_usuario_repository)
):
    """
    Cria um novo usuário no sistema.
    """
    use_case = UsuarioUseCases(usuario_repository)
    return await use_case.criar_usuario(usuario_create)

# Endpoint de autenticação (login)
@router.post(
    "/auth/login",
    response_model=TokenResponse,
    summary="Autenticar usuário"
)
async def login(
    login_request: LoginRequest,
    usuario_repository: UsuarioRepositoryInterface = Depends(get_usuario_repository)
):
    """
    Autentica um usuário e retorna um token de acesso.
    """
    use_case = UsuarioUseCases(usuario_repository)
    return await use_case.autenticar_usuario(login_request.email, login_request.senha)

# Endpoint para obter dados do usuário autenticado
@router.get(
    "/usuarios/me",
    response_model=UsuarioResponse,
    summary="Obter usuário atual"
)
async def obter_usuario_atual(
    current_user: Annotated[Usuario, Depends(get_current_user)]
):
    """
    Retorna os dados do usuário autenticado.
    """
    return UsuarioResponse(
        id=current_user.id,
        email=current_user.email,
        nome=current_user.nome,
        perfil=current_user.perfil,
        ativo=current_user.ativo,
        data_criacao=current_user.data_criacao,
        data_atualizacao=current_user.data_atualizacao,
        ultimo_login=current_user.ultimo_login
    )

# Endpoint para atualizar dados do usuário autenticado
@router.put(
    "/usuarios/me",
    response_model=UsuarioResponse,
    summary="Atualizar usuário atual"
)
async def atualizar_usuario_atual(
    usuario_update: UsuarioUpdate,
    current_user: Annotated[Usuario, Depends(get_current_user)],
    usuario_repository: UsuarioRepositoryInterface = Depends(get_usuario_repository)
):
    """
    Atualiza os dados do usuário autenticado.
    """
    # Não permitir que usuários comuns alterem o perfil
    if usuario_update.perfil is not None and usuario_update.perfil != current_user.perfil:
        usuario_update.perfil = current_user.perfil
    
    use_case = UsuarioUseCases(usuario_repository)
    return await use_case.atualizar_usuario(current_user.id, usuario_update)

# -- Rotas de administração (apenas para admins) --

# Endpoint para listar todos os usuários
@router.get(
    "/admin/usuarios",
    response_model=List[UsuarioResponse],
    summary="Listar todos os usuários (admin)"
)
async def listar_usuarios(
    skip: int = 0,
    limit: int = 100,
    _: Annotated[Usuario, Depends(get_current_admin_user)], # Usuário admin autenticado
    usuario_repository: UsuarioRepositoryInterface = Depends(get_usuario_repository)
):
    """
    Lista todos os usuários (requer privilégios de administrador).
    """
    use_case = UsuarioUseCases(usuario_repository)
    return await use_case.listar_usuarios(skip, limit)

# Endpoint para obter dados de um usuário específico
@router.get(
    "/admin/usuarios/{usuario_id}",
    response_model=UsuarioResponse,
    summary="Obter dados de um usuário (admin)"
)
async def obter_usuario(
    usuario_id: UUID,
    _: Annotated[Usuario, Depends(get_current_admin_user)], # Usuário admin autenticado
    usuario_repository: UsuarioRepositoryInterface = Depends(get_usuario_repository)
):
    """
    Retorna os dados de um usuário específico (requer privilégios de administrador).
    """
    use_case = UsuarioUseCases(usuario_repository)
    return await use_case.obter_usuario(usuario_id)

# Endpoint para atualizar dados de um usuário específico
@router.put(
    "/admin/usuarios/{usuario_id}",
    response_model=UsuarioResponse,
    summary="Atualizar um usuário (admin)"
)
async def atualizar_usuario(
    usuario_id: UUID,
    usuario_update: UsuarioUpdate,
    _: Annotated[Usuario, Depends(get_current_admin_user)], # Usuário admin autenticado
    usuario_repository: UsuarioRepositoryInterface = Depends(get_usuario_repository)
):
    """
    Atualiza os dados de um usuário específico (requer privilégios de administrador).
    """
    use_case = UsuarioUseCases(usuario_repository)
    return await use_case.atualizar_usuario(usuario_id, usuario_update)

# Endpoint para remover um usuário
@router.delete(
    "/admin/usuarios/{usuario_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover um usuário (admin)"
)
async def remover_usuario(
    usuario_id: UUID,
    _: Annotated[Usuario, Depends(get_current_admin_user)], # Usuário admin autenticado
    usuario_repository: UsuarioRepositoryInterface = Depends(get_usuario_repository)
):
    """
    Remove um usuário (requer privilégios de administrador).
    """
    use_case = UsuarioUseCases(usuario_repository)
    await use_case.remover_usuario(usuario_id)
    return None