# src/core/entities/user.py

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr

from bson import ObjectId


class User(BaseModel):
    id: Optional[UUID] = None
    username: str
    email: EmailStr
    hashed_password: str
    profile_picture: Optional[str] = None
    interests: Optional[list[str]] = []

    class Config:
        json_encoders = {
            UUID: lambda v: str(v)
        }
