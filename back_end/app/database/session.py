from sqlalchemy.orm import sessionmaker
from app.database.connection import engine

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

Base = declarative_base()

# tabels
class User(Base):
	id = Column("id", Integer, primary_key=True, index=True)
	name = Column("name", String(150), not_null=True)
	email = Column("email", String(150), not_null=True, unique=True)
	password_hash = Column("password_hash", Text, not_null=True)
	is_active = Column("is_active", Boolean, default=True)
	created_at = Column("created_at", DateTime)


Base.create_all(bind=engine)