from abc import ABC, abstractmethod
from typing import Optional, List, Any

from src.domain.models import User


class UserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User:
        pass

    @abstractmethod
    async def find_by_id(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    async def update(self, user: User) -> Optional[User]:
        pass

    @abstractmethod
    async def delete(self, user_id: str) -> Any:
        pass

    @abstractmethod
    async def list_cards(self, user_id: str) -> Optional[List[User]]:
        pass

    @abstractmethod
    async def list_users(self):
        pass