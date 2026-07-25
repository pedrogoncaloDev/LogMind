from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class LogFileResponse(BaseModel):
    id: UUID
    user_id: UUID
    original_filename: str
    stored_filename: str
    file_size: int = Field(..., description="Tamanho do arquivo em bytes")
    status: str
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)
