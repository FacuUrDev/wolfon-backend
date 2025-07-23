
# SubscriptionService.py
class SubscriptionService:
    def __init__(self, subscription_repo):
        self.subscription_repo = subscription_repo

    async def create_subscription(self, subscription_data):
        return await self.subscription_repo.create(subscription_data)