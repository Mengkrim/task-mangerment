from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional

# Base class for shared fields
class UserCreate(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v.encode('utf-8')) > 72:
            raise ValueError("Password is too long (maximum 72 bytes in UTF-8)")
        return v

# Used for API response
class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool
    created_at: datetime  # fixed typo (was create_at)

    class Config:
        from_attributes = True  # for ORM models

# Internal model for DB only (never expose hashed_password in API responses)
class UserInDB(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    hashed_password: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# For login response (JWT token)
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
