import uuid

from sqlalchemy import Boolean, DateTime, String, Text, Column, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.base import Base


class User(Base):
	__tablename__ = "users"

	id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
	log_files = relationship("LogFile", back_populates="user", cascade="all, delete-orphan")
	name = Column(String(150), nullable=False)
	email = Column(String(150), nullable=False, unique=True)
	password_hash = Column(Text, nullable=False)
	is_active = Column(Boolean, default=True, nullable=False)
	created_at = Column(DateTime, server_default=func.now(), nullable=False)
	updated_at = Column(DateTime, server_default=func.now(), nullable=False)

