from typing import Optional

from src.domain.models import Card
from src.domain.repositories.card_repository import CardRepository


class CardService:
    def __init__(self, card_repository: CardRepository):
        self.card_repository = card_repository

    async def create_card(self, card: Card) -> Card:
        # Lógica de negocio aquí
        return await self.card_repository.create(card)

    async def get_card(self, card_id: str) -> Optional[Card]:
        return await self.card_repository.find_by_id(card_id)

    async def update_card(self, card_id: str, card: Card) -> Optional[Card]:
        card.id = card_id
        return await self.card_repository.update(card)

    async def delete_card(self, card_id: str) -> bool:
        return await self.card_repository.delete(card_id)

#
# if __name__ == "__main__":
#     from src.infrastructure.repositories.mongo_card_repository import MongoCardRepository
#     from src.infrastructure.dependencies.database import get_database
#     card = Card(title="Card 1", user_id="1")
#     card_service = CardService(MongoCardRepository(get_database()))
#     print(await card_service.get_card('686e87c38b36c6e760c635df'))
