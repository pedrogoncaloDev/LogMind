from fastapi import APIRouter
from app.schemas.user_schemas import UserCreate, UserResponse, LoginRequest, TokenResponse
from app.services import user_service
from app.schemas.user_schemas import RefreshTokenRequest

router = APIRouter()


@router.post("", response_model=UserResponse)
def create_user(user: UserCreate):
    return user_service.create_user(user)


@router.post("/login", response_model=TokenResponse)
def login_user(login_request: LoginRequest):
    return user_service.login_user(login_request.email, login_request.password)


@router.post("/token/refresh", response_model=TokenResponse)
def refresh_token(request: RefreshTokenRequest):
    return user_service.refresh_access_token(request.refresh_token)