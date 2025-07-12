from src.domain.models import User
from src.domain.repositories.user_repository import UserRepository


class MongoUserRepository(UserRepository):
    def __init__(self, db):
        self.db = db

    async def create(self, user: User) -> User:
        return self.db.users.insert_one(user.model_dump())

    async def find_by_id(self, user_id: str) -> User:
        return self.db.users.find_one({"_id": user_id})

    async def update(self, user: User) -> User:
        return self.db.users.update_one({"_id": user.id}, {"$set": user.model_dump()})

    async def delete(self, user_id: str) -> bool:
        return self.db.users.delete_one({"_id": user_id})

    async def list_cards(self, user_id: str) -> User:
        return self.db.cards.find({"user_id": user_id})

    async def list_users(self):
        return list(self.db.users.find({}))

if __name__ == '__main__':
    from src.infrastructure.dependencies.database import get_database
    RUser = MongoUserRepository(get_database())
    RUser.db.users.find_one({'_id':'6871a6974530f72a169057e3'})