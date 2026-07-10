from fastapi import APIRouter
from app.domains.users import service as user_service
from .schema import UserCreate, UserResponse, LoginRequest, TokenResponse, RefreshTokenRequest

router = APIRouter()


@router.post(
    "",
    response_model=UserResponse,
    summary="Criar novo usuário",
    description="Registra um novo usuário no sistema",
    responses={
        201: {"description": "Usuário criado com sucesso"},
        409: {"description": "Email já existe"},
        422: {"description": "Dados inválidos"}
    }
)
def create_user(user: UserCreate):
    """
    Cria um novo usuário.
    
    - **name**: Nome do usuário (mínimo 1 caractere)
    - **email**: Email válido e único
    - **password**: Senha com mínimo 8 caracteres
    - **is_active**: Se o usuário está ativo (padrão: true)
    """
    return user_service.create_user(user)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login de usuário",
    description="Autentica o usuário e retorna access_token e refresh_token",
    responses={
        200: {"description": "Login bem-sucedido"},
        400: {"description": "Email ou senha incorretos"}
    }
)
def login_user(login_request: LoginRequest):
    """
    Realiza login do usuário.
    
    Retorna:
    - **access_token**: Token JWT válido por 15 minutos
    - **refresh_token**: Token válido por 7 dias
    - **token_type**: Tipo de token (sempre "bearer")
    """
    return user_service.login_user(login_request.email, login_request.password)


@router.post(
    "/token/refresh",
    response_model=TokenResponse,
    summary="Renovar access token",
    description="Usa o refresh_token para obter um novo access_token",
    responses={
        200: {"description": "Token renovado com sucesso"},
        400: {"description": "Refresh token inválido ou expirado"}
    }
)
def refresh_token(request: RefreshTokenRequest):
    """
    Renova o access_token usando o refresh_token.
    
    Use quando o access_token expirar (após 15 minutos).
    """
    return user_service.refresh_access_token(request.refresh_token)