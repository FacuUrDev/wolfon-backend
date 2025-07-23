from datetime import UTC, datetime, timedelta

from src.application.interfaces.subscription_interface import SubscriptionInterface
from src.domain import Subscription
from src.domain.subscription_model import SubscriptionStatus


class SubscriptionRepository(SubscriptionInterface):
    def __init__(self, db):
        self.db = db

    def create(self, sub: Subscription) -> str:
        created_sub = self.db.subscriptions.insert_one(sub)
        if created_sub is None:
            raise Exception("Failed to create subscription")
        return created_sub.inserted_id

    def renew(self, sub: Subscription) -> Subscription:
        state = sub["state"]
        state["valid_to"] = datetime.now(UTC) + timedelta(days=30)
        state["status"] = SubscriptionStatus.active
        sub["state"] = state
        return sub

    def cancel(self, sub: Subscription) -> Subscription:
        state = sub["state"]
        state["valid_to"] = datetime.now(UTC)
        state["status"] = SubscriptionStatus.cancelled
        sub["state"] = state
        return sub

    def is_active(self, sub: Subscription) -> bool:
        state = sub["subscription"]["state"]
        if state.get("valid_to") is None or state.get("valid_to") > datetime.now(UTC):
            if state.get("status") != SubscriptionStatus.active:
                state["status"] = SubscriptionStatus.active
                sub["subscription"]["state"] = state
            return True
        return False
