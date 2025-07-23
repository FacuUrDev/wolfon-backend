from fastapi import APIRouter, Body

from src.application.services.subscription_service import SubscriptionService
from src.infrastructure import get_database
from src.infrastructure.repositories.subscription_repository import SubscriptionRepository

router = APIRouter()
subscription_service = SubscriptionService(SubscriptionRepository(get_database()))


@router.post("/create", description="Create a new subscription tier")
async def cancel_subscription(data=Body(...)):
    return await subscription_service.create_subscription(data)
