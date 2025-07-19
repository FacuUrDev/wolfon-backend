from datetime import UTC, datetime
from typing import Any

from src.domain.models import User
from src.application.interfaces.user_interface import UserInterface
from bson import ObjectId

class MongoUserInterface(UserInterface):
    def __init__(self, db):
        self.db = db

    async def create(self, user: Any):
        if isinstance(user, User):
            user = user.model_dump()
        user['created_at'] = datetime.now(UTC)
        insert_result = self.db.users.insert_one(user)
        return insert_result.inserted_id

    async def find_by_id(self, user_id: str) -> User:
        return self.db.users.find_one({"_id": ObjectId(user_id)})

    async def update(self, user: Any):
        if isinstance(user, User):
            user = user.model_dump()
        user['updated_at'] = datetime.now(UTC)
        if '_id' not in user:
            raise KeyError(f'Expected "_id" key in user data. Received {user}')
        _id = user['_id']
        del user['_id']
        return self.db.users.update_one({"_id": ObjectId(_id)}, {"$set": user})

    async def delete(self, user_id: str) -> bool:
        return self.db.users.delete_one({"_id": ObjectId(user_id)})

    async def list_cards(self, user_id: str) -> User:
        return self.db.cards.find({"user_id": user_id})

    async def list_users(self):
        return list(self.db.users.find({}))

if __name__ == '__main__':
    from src.infrastructure.dependencies.database import get_database
    RUser = MongoUserInterface(get_database())
    RUser.db.users.find_one({'_id':'6871a6974530f72a169057e3'})