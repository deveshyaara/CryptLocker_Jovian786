"""
User Model
Represents a holder (wallet user) in the system
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user model"""
    email: EmailStr
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    username: str = Field(..., min_length=3, max_length=50)


class UserCreate(UserBase):
    """User creation model"""
    password: str = Field(..., min_length=8, max_length=128)


class UserUpdate(BaseModel):
    """User update model"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    password: Optional[str] = Field(None, min_length=8, max_length=128)


class UserLogin(BaseModel):
    """User login model"""
    username: str
    password: str


class User(UserBase):
    """Complete user model"""
    id: int
    did: Optional[str] = None
    wallet_id: Optional[str] = None
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserInDB(User):
    """User model with hashed password (internal use)"""
    hashed_password: str


class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"
    user: User


class TokenData(BaseModel):
    """Token payload data"""
    user_id: int
    username: str
    exp: datetime
