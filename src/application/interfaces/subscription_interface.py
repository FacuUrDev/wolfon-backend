from abc import ABC, abstractmethod

from src.domain.subscription_model import Subscription


class SubscriptionInterface(ABC):
    @abstractmethod
    def create(self, tier: str) -> Subscription:
        pass

    @abstractmethod
    def renew(self, sub: Subscription) -> Subscription:
        pass

    @abstractmethod
    def cancel(self, sub: Subscription) -> Subscription:
        pass

    @abstractmethod
    def is_active(self, sub: Subscription) -> bool:
        pass
