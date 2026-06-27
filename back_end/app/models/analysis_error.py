import uuid

from sqlalchemy import (Integer, Boolean, DateTime, String, Text, Column, func, BigInteger, ForeignKey)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.base import Base


class AnalysisError(Base):
    __tablename__ = "analysis_error"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    analysis_id = Column(UUID(as_uuid=True), ForeignKey("analysis.id"), nullable=False)
    error_name = Column(String(500), nullable=False, default=0)
    occurrences = Column(Integer)
    severity = Column(String(20))
    possible_cause = Column(Text, nullable=False)
    recommendation = Column(Text, nullable=False)
