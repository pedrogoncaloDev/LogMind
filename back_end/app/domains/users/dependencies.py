from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.security import verify_access_token
from . import repository as user_repository
from .model import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

CREDENTIALS_EXCEPTION = HTTPException(
	status_code=status.HTTP_401_UNAUTHORIZED,
	detail="Credenciais inválidas ou expiradas",
	headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
	payload = verify_access_token(token)
	if not payload:
		raise CREDENTIALS_EXCEPTION

	user_id = payload.get("sub")
	if not user_id:
		raise CREDENTIALS_EXCEPTION

	user = user_repository.find_by_id(user_id=user_id)
	if not user:
		raise CREDENTIALS_EXCEPTION

	if not user.is_active:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="Usuário inativo",
		)

	return user
