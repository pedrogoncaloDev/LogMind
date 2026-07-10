from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic_core import PydanticCustomError 
from uuid import UUID


class PasswordMixin(BaseModel):
    password: str = Field(...)

    @field_validator("password", mode="before")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise PydanticCustomError(
                "password.too_short",
                "A senha deve ter pelo menos 8 caracteres."
            )
        return value


class UserCreate(PasswordMixin):
    name: str = Field(..., min_length=1)
    email: EmailStr
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
    id: UUID
    name: str = Field(..., min_length=1)
    email: EmailStr
    is_active: bool = True
    updated_at: str = Field(..., description="Data de atualização do usuário")

    class Config:
        from_attributes = True


class LoginRequest(PasswordMixin):
    email: EmailStr = Field(..., example="user@example.com")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "senha123456"
            }
        }


class TokenResponse(BaseModel):
    access_token: str = Field(..., example="eyJhbGc...")
    token_type: str = Field(default="bearer", example="bearer")
    refresh_token: str = Field(..., example="eyJhbGc...")
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }


class RefreshTokenRequest(BaseModel):
    refresh_token: str