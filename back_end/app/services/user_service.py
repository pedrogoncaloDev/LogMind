import app.repositories.user_repository as user_repository

def create_user(user_data: dict) -> User:
	return user_repository.create_user(user_data)