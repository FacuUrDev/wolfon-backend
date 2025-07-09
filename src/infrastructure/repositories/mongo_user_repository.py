from bson import ObjectId

from src.domain.models import User
from src.domain.repositories.user_repository import UserRepository


class MongoUserRepository(UserRepository):
    def __init__(self, db):
        self.db = db

    async def create(self, user: User) -> User:
        return self.db.users.insert_one(user.model_dump())

    async def find_by_id(self, user_id: str) -> User:
        return self.db.users.find_one({"_id": ObjectId(user_id)})

    async def update(self, user: User) -> User:
        return self.db.users.update_one({"_id": ObjectId(user.id)}, {"$set": user.model_dump(exclude={'_id'})})

    async def delete(self, user_id: str) -> bool:
        return self.db.users.delete_one({"_id": ObjectId(user_id)})

    async def list_cards(self, user_id: str) -> User:
        return self.db.cards.find({"user_id": ObjectId(user_id)})