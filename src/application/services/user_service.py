from typing import Optional, Any

from src.domain.models import User
from src.domain.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, user: User) -> User:
        # Lógica de negocio aquí
        return await self.user_repository.create(user)

    async def get_user(self, user_id: str) -> Optional[User]:
        return await self.user_repository.find_by_id(user_id)

    async def update_user(self, user_id: str, user: User) -> Optional[User]:
        user.id = user_id
        return await self.user_repository.update(user)

    async def delete_user(self, user_id: str) -> bool:
        return await self.user_repository.delete(user_id)

    async def list_cards(self, user_id: str) -> list:
        cards = await self.user_repository.list_cards(user_id)

        # Repositorio devuelve BSON ObjectId, que Pydantic no puede serializar a JSON por defecto .
        # Convertimos el  '_id' (ObjectId)  a string 'id'.
        processed_cards = []
        for card in cards:
            
            if '_id' in card:
                card['id'] = str(card.pop('_id'))
            processed_cards.append(card)

        return processed_cards
