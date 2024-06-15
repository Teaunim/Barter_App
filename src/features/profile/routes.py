# src/features/profile/routes.py
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from src.core.entities.user import User
from src.features.profile.profile_service import update_interests, update_profile_picture, update_user_info

profile_router = APIRouter()


class InterestsUpdateRequest(BaseModel):
    interests: List[str]


class ProfilePictureUpdateRequest(BaseModel):
    profile_picture_url: str


class UserUpdateRequest(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    hashed_password: str
    interests: Optional[List[str]] = []
    profile_picture: Optional[str] = None


@profile_router.put("/update_interests/{user_id}", response_model=User)
def update_user_interests(user_id: UUID, interests_update_request: InterestsUpdateRequest):
    updated_user = update_interests(user_id, interests_update_request.interests)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated_user


@profile_router.put("/update_profile_picture/{user_id}", response_model=User)
def update_user_profile_picture(user_id: UUID, profile_picture_update_request: ProfilePictureUpdateRequest):
    updated_user = update_profile_picture(user_id, profile_picture_update_request.profile_picture_url)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated_user


@profile_router.put("/update_user", response_model=User)
def update_user(user_update_request: UserUpdateRequest):
    updated_user = User(**user_update_request.dict())
    updated_user = update_user_info(updated_user)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated_user
