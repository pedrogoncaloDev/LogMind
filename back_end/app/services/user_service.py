from datetime import timedelta
import app.repositories.user_repository as user_repository
from app.schemas.user_schemas import UserResponse, TokenResponse
from app.core.security import verify_password, create_access_token, create_refresh_token, verify_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import HTTPException
from starlette.status import HTTP_409_CONFLICT, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR


def create_user(user_data: dict) -> UserResponse:
	try:
		return user_repository.create_user(user_data)
	except ValueError as e:
		raise HTTPException(status_code=HTTP_409_CONFLICT, detail=str(e))
	except Exception:
		raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno no servidor")


def login_user(email: str, password: str) -> TokenResponse:
	try:
		user = user_repository.find_by_email(email=email)

		if not user:
			raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Email incorreto ou usuário não encontrado")

		if not verify_password(password, user.password_hash):
			raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Senha incorreta")

		if not user.is_active:
			raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Usuário inativo")
		
		# Criar tokens
		access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
		access_token = create_access_token(
			data={"sub": str(user.id), "email": user.email},
			expires_delta=access_token_expires
		)
		refresh_token = create_refresh_token(
			data={"sub": str(user.id), "email": user.email}
		)
		
		return TokenResponse(
			access_token=access_token,
			refresh_token=refresh_token,
			token_type="bearer"
		)
	except HTTPException:
		raise
	except Exception:
		raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno no servidor")


def refresh_access_token(refresh_token: str) -> TokenResponse:
	try:
		payload = verify_access_token(refresh_token)
		
		if not payload:
			raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Refresh token inválido ou expirado")
		
		user_id = payload.get("sub")
		email = payload.get("email")
		
		if not user_id or not email:
			raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Token inválido")
		
		# Criar novo access token
		access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
		new_access_token = create_access_token(
			data={"sub": user_id, "email": email},
			expires_delta=access_token_expires
		)
		
		return TokenResponse(
			access_token=new_access_token,
			refresh_token=refresh_token,
			token_type="bearer"
		)
	except HTTPException:
		raise
	except Exception:
		raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno no servidor")