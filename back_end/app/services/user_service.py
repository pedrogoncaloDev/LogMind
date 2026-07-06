import app.repositories.user_repository as user_repository
from app.schemas.user_schemas import UserResponse

def create_user(user_data: dict) -> UserResponse:
	return user_repository.create_user(user_data)