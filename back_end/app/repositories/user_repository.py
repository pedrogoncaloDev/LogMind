from app.database.user_repository import SessionLocal

def find_by_email(db: Session, email: str):
	try:
		return (
			db.query(User)
			.filter(User.email == email)
			.first()
		)
	except Exception as e:
		raise e


def create_user(user_data: dict) -> User:
	try:
		with SessionLocal() as db:
			existing_user = user_repository.find_by_email(db, user_data['email'])
			if existing_user:
				raise ValueError("Já existe um usuário com este e-mail.")
		
			new_user = User(**user_data)
			db.add(new_user)
			db.commit()
			db.refresh(new_user)
			return new_user
	except Exception as e:
		db.rollback()
		raise e