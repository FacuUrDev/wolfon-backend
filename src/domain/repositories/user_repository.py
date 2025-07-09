from abc import ABC, abstractmethod
from typing import Optional, List

from src.domain.models import User


class UserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User:
        pass

    @abstractmethod
    async def find_by_id(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    async def update(self, user_id: str, user: User) -> Optional[User]:
        pass

    @abstractmethod
    async def delete(self, user_id: str) -> bool:
        pass

    @abstractmethod
    async def list_cards(self, user_id: str) -> Optional[List[User]]:
        pass
