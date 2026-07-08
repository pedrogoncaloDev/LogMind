import app.repositories.user_repository as user_repository
from app.schemas.user_schemas import UserResponse
from fastapi import HTTPException
from app.core.security import hash_password, verify_password
from starlette.status import HTTP_409_CONFLICT, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR


def create_user(user_data: dict) -> UserResponse:
	try:
		return user_repository.create_user(user_data)
	except ValueError as e:
		# Valor levantado quando o e-mail já existe; retornar 409 Conflict
		raise HTTPException(status_code=HTTP_409_CONFLICT, detail=str(e))
	except Exception:
		# Para quaisquer outros erros, retornar 500 genérico
		raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno no servidor")


def login_user(email: str, password: str) -> UserResponse:
	try:
		user = user_repository.find_by_email(email)

		if not user:
			raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Email incorreto ou usuário não encontrado")

		if not verify_password(password, user.password_hash):
			raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Senha incorreta")

		if not user.is_active:
			raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Usuário inativo")
		
		return UserResponse(
			id=user.id,
			name=user.name,
			email=user.email,
			password_hash=user.password_hash,
			is_active=user.is_active,
			updated_at=str(user.updated_at),
		)
	except HTTPException:
		raise
	except Exception:
		raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno no servidor")