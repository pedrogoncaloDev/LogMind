from sqlalchemy.orm import sessionmaker
from app.database.connection import engine
from app.database.base import Base
from app.domains.users.model import User
from app.domains.log_files.model import LogFile
from app.domains.analysis.model import Analysis
from app.domains.analysis_error.model import AnalysisError


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)