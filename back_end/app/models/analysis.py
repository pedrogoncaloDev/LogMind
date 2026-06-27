import uuid

from sqlalchemy import (Integer, Boolean, DateTime, String, Text, Column, func, BigInteger, ForeignKey)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.base import Base


class Analysis(Base):
    __tablename__ = "analysis"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    log_file_id = Column(UUID(as_uuid=True), ForeignKey("log_files.id"), nullable=False)
    total_lines = Column(Integer, nullable=False, default=0)
    total_errors = Column(Integer, nullable=False, default=0)
    total_warnings = Column(Integer, nullable=False, default=0)
    ai_summary = Column(Text, nullable=False)
    processing_time_ms = Column(BigInteger)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
