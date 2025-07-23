from datetime import UTC, datetime
from typing import Any

from bson import ObjectId

from src.application.interfaces.user_interface import UserInterface
from src.domain.user_model import User


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

    async def search(self, filter: dict):
        return list(self.db.users.find(filter))


if __name__ == '__main__':
    from src.infrastructure.dependencies.database import get_database
    from pprint import pp

    RUser = MongoUserInterface(get_database())
    RUser.db.users.find_one({'_id': '6871a6974530f72a169057e3'})
    db = get_database()
    pp(list(db.users.aggregate([{
        "$lookup": {
            "from": "cards",
            "localField": {"_id": {"$toString": "_id"}},
            "foreignField": "user_id",
            "as": "user_card",
        }
    }])))
    pp(list(db.users.aggregate([{
        "$lookup": {
            "from": "cards",
            "let": {"userId": {"$toString": "$_id"}},
            "pipeline": [
                {"$match": {"$expr": {"$eq": ["$user_id", "$$userId"]}}}
            ],
            "as": "user_cards",
        }},
        {"$sort": {"created_at": 1}}
    ], explain=True)))
