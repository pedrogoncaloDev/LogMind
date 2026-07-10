import uuid

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.base import Base


class LogFile(Base):
	__tablename__ = "log_files"

	id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
	original_filename = Column(String(255), nullable=False)
	stored_filename = Column(String(255), nullable=False)
	file_size = Column(BigInteger, nullable=False)
	status = Column(String(30), nullable=False)
	uploaded_at = Column(DateTime, server_default=func.now(), nullable=False)

	user = relationship("User", back_populates="log_files")
