from fastapi import APIRouter
from app.schemas.user_schemas import UserCreate, UserResponse
from app.services import user_service

router = APIRouter()	

@router.post("", response_model=UserResponse)
def create_user(user: UserCreate):
    return user_service.create_user(user)
