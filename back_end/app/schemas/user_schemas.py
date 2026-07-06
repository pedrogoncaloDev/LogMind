from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
	name: str = Field(..., min_length=1)
	email: EmailStr
	password_hash: str = Field(..., min_length=8)
	is_active: bool = True
	created_at: datetime = Field(
		default_factory=datetime.now,
		description="Data de criação do usuário"
	)
	updated_at: datetime = Field(
		default_factory=datetime.now,
		description="Data de atualização do usuário"
	)


class UserResponse(BaseModel):
	id: int
	name: str = Field(..., min_length=1)
	email: EmailStr
	password_hash: str = Field(..., min_length=8)
	is_active: bool = True
	updated_at: str = Field(..., description="Data de atualização do usuário")

	class Config:
		from_attributes = True