from sqlalchemy.orm import sessionmaker

from app.database.connection import engine
from app.database.base import Base
from app.models import log_file, user

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

Base.metadata.create_all(bind=engine)