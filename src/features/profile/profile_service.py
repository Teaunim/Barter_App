# src/features/profile/profile_service.py
from uuid import UUID

from src.infrastructure.repositories.mongo_user_repository import MongoUserRepository
from src.core.entities.user import User
from src.infrastructure.database import users_collection
from bson import ObjectId, Binary, UuidRepresentation

user_repository = MongoUserRepository(users_collection)


def update_interests(user_id: UUID, interests: list[str]) -> User:
    user = user_repository.collection.find_one(
        {"id": Binary.from_uuid(user_id, uuid_representation=UuidRepresentation.STANDARD)})
    if not user:
        return None

    user["interests"] = interests
    updated_user = User(**user)
    return user_repository.update_user(updated_user)


def update_profile_picture(user_id: UUID, profile_picture_url: str) -> User:
    user = user_repository.collection.find_one(
        {"id": Binary.from_uuid(user_id, uuid_representation=UuidRepresentation.STANDARD)})
    if not user:
        return None
    user["profile_picture"] = profile_picture_url
    updated_user = User(**user)
    return user_repository.update_user(updated_user)


def update_user_info(user: User) -> User:
    existing_user = user_repository.get_user_by_email(user.email)
    if not existing_user:
        return None
    return user_repository.update_user(user)
