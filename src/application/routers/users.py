from fastapi import APIRouter, Body, Response, HTTPException, status

from src.application.services.user_service import UserService
from src.domain import User, Card
from src.infrastructure import get_database, logger
from src.infrastructure.repositories.mongo_user_repository import MongoUserInterface
from src.infrastructure.repositories.subscription_repository import SubscriptionRepository

router = APIRouter(
    prefix="/users",
    tags=["users"]
)
database = get_database()
logger.info("Initializing user service", database=database)
user_service = UserService(MongoUserInterface(database))
subscription_repository = SubscriptionRepository(database)


@router.post("/", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(user: User):
    if (inserted_id := await user_service.create_user(user)) is not None:
        await logger.ainfo("User created successfully", inserted_id=inserted_id)
        user.id = str(inserted_id)
        return user
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")


@router.get("/list_cards/{user_id}", response_description="List cards for a user", response_model=list[Card])
async def list_cards(user_id: str, page: int = 1, size: int = 10):
    await logger.ainfo("Listing cards for user", user_id=user_id)
    if (cards := await user_service.list_cards(user_id, page, size)) is not None:
        for i, _ in enumerate(cards):
            cards[i]['_id'] = str(cards[i]['_id'])
        return cards
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")


@router.get("/list", response_description="List all users", response_model=list[User])
async def list_users(page: int = 1, size: int = 10):
    users_list = list(await user_service.list_users(page, size))
    await logger.ainfo("Listing users", users_list=users_list)
    for i, user in enumerate(users_list):
        users_list[i]['_id'] = str(user['_id'])
    return users_list
    # return await user_service.list_users()


@router.get("/{user_id}", response_description="Get a single user by id")
async def find_user(user_id: str):
    user = await user_service.get_user(user_id)
    await logger.ainfo("User found", user=user)
    if user is not None:
        user['_id'] = user_id
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} not found")


@router.put("/", response_description="Update a user")
async def update_user(user=Body(...)):
    await logger.ainfo("Updating user", user=user)
    updated_user = await user_service.update_user(user)
    if updated_user.modified_count > 0:
        await logger.ainfo("User updated successfully", user=updated_user)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    await logger.ainfo("User not found", user=user)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user} not found")


@router.post("/subscribe", response_description="Subscribe a user")
async def subscribe_user(body=Body(...)):
    user_id: str = body.get("user_id")
    tier: str = body.get("tier")
    valid_from = body.get("valid_from")
    valid_to = body.get("valid_to")
    subscribed_user = await user_service.subscribe(user_id, tier, valid_from, valid_to)
    if subscribed_user.modified_count > 0:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")


@router.delete("/{id}", response_description="Delete a user")
async def delete_user(id: str):
    deleted_user = await user_service.delete_user(id)
    if deleted_user.deleted_count > 0:
        await logger.ainfo("User deleted", user=deleted_user)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")


@router.get("/check_subscription/{user_id}", response_description="Check subscription status for a user")
async def check_subscription(user_id: str):
    user = await user_service.get_user(user_id)
    if user is not None:
        return user.get("subscription", {})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} not found")


@router.get("/cancel_subscription/{user_id}", response_description="Cancel subscription for a user")
async def cancel_subscription(user_id: str):
    user = await user_service.get_user(user_id)
    user["subscription"] = subscription_repository.cancel(user["subscription"])
    cancelled_user = await user_service.update_user(user)
    if cancelled_user.modified_count > 0:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} not found")


@router.get("/renew_subscription/{user_id}", response_description="Renew subscription for a user")
async def renew_subscription(user_id: str):
    user = await user_service.get_user(user_id)
    user["subscription"] = subscription_repository.renew(user["subscription"])
    renewed_user = await user_service.update_user(user)
    if renewed_user.modified_count > 0:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} not found")
