# src/features/auth/routes.py
from typing import Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from src.core.entities.user import User
from src.infrastructure.repositories.mongo_user_repository import MongoUserRepository
from src.infrastructure.database import users_collection


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    interests: Optional[list[str]] = []


auth_router = APIRouter()
user_repository = MongoUserRepository(users_collection)


@auth_router.post("/register", response_model=User)
def register(user: UserCreate):
    existing_user = user_repository.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    new_user = User(**user.dict())
    return user_repository.create_user(new_user)
