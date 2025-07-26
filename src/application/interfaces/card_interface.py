from abc import ABC, abstractmethod
from typing import Optional, Any, List

from src.domain import Card


class CardInterface(ABC):
    @abstractmethod
    async def create(self, card: Any) -> Card:
        pass

    @abstractmethod
    async def find_by_id(self, card_id: str) -> Optional[Card]:
        pass

    @abstractmethod
    async def update(self, card: Any) -> Optional[Card]:
        pass

    @abstractmethod
    async def delete(self, card_id: str) -> bool:
        pass

    async def bulk_create(self, cards: list[dict[str, Any]]):
        pass
