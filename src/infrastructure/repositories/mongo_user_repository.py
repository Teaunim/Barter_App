# src/infrastructure/repositories/mongo_user_repository.py
from uuid import uuid4, UUID

from pymongo.collection import Collection
from src.core.entities.user import User
from bson import ObjectId, Binary, UuidRepresentation


class MongoUserRepository():

    def __init__(self, collection: Collection):
        self.collection = collection

    def create_user(self, user: User) -> User:
        if not user.id:
            user.id = uuid4()
        user_dict = user.dict()
        user_dict['id'] = Binary.from_uuid(user.id, uuid_representation=UuidRepresentation.STANDARD)
        self.collection.insert_one(user_dict)
        return user

    def get_user_by_email(self, email: str) -> User:
        user_dict = self.collection.find_one({"email": email})
        if user_dict:
            return User(**user_dict)
        return None

    def get_user_by_id(self, id: UUID)-> User:
        user_dict = self.collection.find_one({"id": Binary.from_uuid(id, uuid_representation=UuidRepresentation.STANDARD)})

        if user_dict:
            return User(**user_dict)
        return None

    def update_user(self, user: User) -> User:
        user_dict = user.dict()
        user_dict['id'] = Binary.from_uuid(user.id, uuid_representation=UuidRepresentation.STANDARD)
        if self.get_user_by_id(user.id):
            self.collection.update_one({"id": user_dict['id']}, {"$set": user_dict})
            return user
        return None
