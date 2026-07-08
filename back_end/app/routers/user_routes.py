from fastapi import APIRouter
from app.schemas.user_schemas import UserCreate, UserResponse, LoginRequest
from app.services import user_service

router = APIRouter()	

@router.post("", response_model=UserResponse)
def create_user(user: UserCreate):
    return user_service.create_user(user)


@router.post("/login", response_model=UserResponse)
def login_user(login_request: LoginRequest):
	return user_service.login_user(login_request.email, login_request.password)
