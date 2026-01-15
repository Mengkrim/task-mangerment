from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

# Base class for shared fields
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

# Used for user registration (input)
class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=64)

# Used for API response
class UserOut(UserBase):
    id: int
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
