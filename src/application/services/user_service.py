from typing import Optional, Any

from src.domain.models import User
from src.application.interfaces.user_interface import UserInterface


class UserService:
    def __init__(self, user_repository: UserInterface):
        self.user_repository = user_repository

    async def create_user(self, user: User) -> User:
        # Lógica de negocio aquí
        return await self.user_repository.create(user)

    async def get_user(self, user_id: str) -> Optional[User]:
        return await self.user_repository.find_by_id(user_id)

    async def update_user(self, user: User) -> Optional[User]:
        return await self.user_repository.update(user)

    async def delete_user(self, user_id: str) -> bool:
        return await self.user_repository.delete(user_id)

    async def list_cards(self, user_id: str) -> Optional[Any]:
        cards = await self.user_repository.list_cards(user_id)
        return list(cards)

    async def list_users(self):
        return await self.user_repository.list_users()

if __name__ == '__main__':
    from src.infrastructure.repositories.mongo_user_repository import MongoUserInterface
    from src.infrastructure.dependencies.database import get_database
    import asyncio
    user_service = UserService(user_repository=MongoUserInterface(get_database()))
    asyncio.run(user_service.list_users())