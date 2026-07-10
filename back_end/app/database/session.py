from sqlalchemy.orm import sessionmaker

from app.database.connection import engine
from app.database.base import Base
from app.models import log_file, user, analysis, analysis_error

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)