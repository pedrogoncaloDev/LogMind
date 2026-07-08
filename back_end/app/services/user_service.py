import app.repositories.user_repository as user_repository
from app.schemas.user_schemas import UserResponse
from fastapi import HTTPException
from starlette.status import HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR


def create_user(user_data: dict) -> UserResponse:
	try:
		return user_repository.create_user(user_data)
	except ValueError as e:
		# Valor levantado quando o e-mail já existe; retornar 409 Conflict
		raise HTTPException(status_code=HTTP_409_CONFLICT, detail=str(e))
	except Exception:
		# Para quaisquer outros erros, retornar 500 genérico
		raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno no servidor")