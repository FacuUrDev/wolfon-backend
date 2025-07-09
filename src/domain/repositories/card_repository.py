from abc import ABC, abstractmethod
from typing import Optional

from src.domain.models import Card


class CardRepository(ABC):
    @abstractmethod
    async def create(self, card: Card) -> Card:
        pass

    @abstractmethod
    async def find_by_id(self, card_id: str) -> Optional[Card]:
        pass

    @abstractmethod
    async def update(self, card_id: str, card: Card) -> Optional[Card]:
        pass

    @abstractmethod
    async def delete(self, card_id: str) -> bool:
        pass
