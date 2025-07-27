import io
from datetime import datetime, UTC, timedelta
from typing import Optional, Any

from pandas import DataFrame

from src.application.interfaces.user_interface import UserInterface
from src.domain import User, Subscription
from src.infrastructure.logging.logger import logger
# from src.domain.subscription_model import SubscriptionState
from src.infrastructure.repositories.subscription_repository import SubscriptionRepository


class UserService:
    def __init__(self, user_repository: UserInterface):
        self.user_repository = user_repository
        self.db = user_repository.db
        self.subscription_repository = SubscriptionRepository(self.db)

    async def check_subscription_status(self, user_id: str) -> bool:
        user = await self.get_user(user_id)
        if user is None:
            raise ValueError(f"User with ID {user_id} not found")
        user = User(**dict(user))
        return self.subscription_repository.is_active(user.subscription)

    async def subscribe(self, user_id: str, tier: str, valid_from: datetime = None, valid_to: datetime = None):
        subscription = self.user_repository.db.subscriptions.find_one({"tier": tier})
        if subscription is None:
            raise ValueError(f"Subscription tier {tier} not found")
        subscription["state"] = {
            "valid_from": valid_from if valid_from is not None else datetime.now(UTC),
            "valid_to": valid_to if valid_to is not None else datetime.now(UTC) + timedelta(days=31)
        }
        subscription = Subscription(**subscription)

        user = await self.get_user(user_id)
        user["subscription"] = subscription.model_dump()
        return await self.update_user(user)

    async def create_user(self, user: User) -> User:
        return await self.user_repository.create(user)

    async def get_user(self, user_id: str) -> Optional[User]:
        return await self.user_repository.find_by_id(user_id)

    async def update_user(self, user: User) -> Optional[User]:
        return await self.user_repository.update(user)

    async def delete_user(self, user_id: str) -> bool:
        return await self.user_repository.delete(user_id)

    async def list_cards(self, user_id: str, page, size) -> Optional[Any]:
        cards = await self.user_repository.list_cards(user_id, page, size)
        return list(cards)

    async def list_users(self, page, size):
        return await self.user_repository.list_users(page, size)

    async def export_cards(self, user_id: str) -> bytes:
        page = 1
        size = 100
        cards = []
        _cards = await self.list_cards(user_id, page, size)
        while len(_cards) > 0:
            cards.extend(_cards)
            page += 1
            _cards = await self.list_cards(user_id, page, size)
        logger.info("Exporting cards", cards=len(cards))
        with io.BytesIO() as buffer:
            DataFrame(cards).to_excel(buffer, index=False)
            buffer.seek(0)
            return buffer.read()


if __name__ == '__main__':
    from src.infrastructure.repositories.mongo_user_repository import MongoUserInterface
    from src.infrastructure.dependencies.database import get_database
    import asyncio

    self = UserService(user_repository=MongoUserInterface(get_database("wolfon_dev")))

    print(asyncio.run(self.subscribe("6874b7b0c53d73d0cc957eef", "free")))
    print(asyncio.run(self.subscribe("6874b7b0c53d73d0cc957ef2", "pro")))
