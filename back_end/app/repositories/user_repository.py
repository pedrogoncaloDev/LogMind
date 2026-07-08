from app.database.session import SessionLocal
from app.schemas.user_schemas import UserResponse, UserCreate
from app.models.user import User
from app.core.security import hash_password

def find_by_email(email: str, database_session=None):
	try:
		if database_session is None:
			with SessionLocal() as database_session:
				return (
						database_session.query(User)
							.filter(User.email == email)
							.first()
						)
		
		return (
				database_session.query(User)
						.filter(User.email == email)
						.first()
				)
	except Exception as e:
		raise e


def create_user(user_data: UserCreate) -> UserResponse:
	try:
		with SessionLocal() as database_session:
			if isinstance(user_data, dict):
				email = user_data.get("email")
				name = user_data.get("name")
				password = user_data.get("password")
				is_active = user_data.get("is_active", True)
			else:
				email = user_data.email
				name = user_data.name
				password = user_data.password
				is_active = user_data.is_active
			
			existing_user = find_by_email(database_session, email)
			if existing_user:
				raise ValueError("Já existe um usuário com este e-mail.")

			new_user = User(
				name=name,
				email=str(email),
				password_hash=hash_password(password),
				is_active=is_active,
			)

			database_session.add(new_user)
			database_session.commit()
			database_session.refresh(new_user)

			return UserResponse(
				id=new_user.id,
				name=new_user.name,
				email=new_user.email,
				password_hash=new_user.password_hash,
				is_active=new_user.is_active,
				updated_at=str(new_user.updated_at),
			)
	except Exception as e:
		database_session.rollback()
		raise e