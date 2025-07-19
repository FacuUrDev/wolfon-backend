from fastapi import APIRouter, Body, Response, HTTPException, status

from src.application.services.user_service import UserService
from src.domain.models import User, Card
from src.infrastructure import get_database, logger
from src.infrastructure.repositories.mongo_user_repository import MongoUserInterface

router = APIRouter()
user_service = UserService(MongoUserInterface(get_database()))


@router.post("/", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(user: User):
    if (inserted_id := await user_service.create_user(user)) is not None:
        logger.info("User created successfully", inserted_id=inserted_id)
        user.id = str(inserted_id)
        return user
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")


@router.get("/list_cards/{user_id}", response_description="List cards for a user", response_model=list[Card])
async def list_cards(user_id: str):
    logger.info("Listing cards for user", user_id=user_id)
    if (cards := await user_service.list_cards(user_id)) is not None:
        for i, _ in enumerate(cards):
            cards[i]['_id'] = str(cards[i]['_id'])
        return cards
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")


@router.get("/list", response_description="List all users", response_model=list[User])
async def list_users():
    users_list = await user_service.list_users()
    for i, user in enumerate(users_list):
        user['_id'] = str(user['_id'])
    return users_list
    # return await user_service.list_users()


@router.get("/{user_id}", response_description="Get a single user by id")
async def find_user(user_id: str):
    user = await user_service.get_user(user_id)
    logger.info("User found", user=user)
    if user is not None:
        user['_id'] = user_id
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} not found")


@router.put("/", response_description="Update a user")
async def update_user(user = Body(...)):
    updated_user = await user_service.update_user(user)
    if updated_user.modified_count > 0:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")


@router.delete("/{id}", response_description="Delete a user")
async def delete_user(id: str):
    deleted_user = await user_service.delete_user(id)
    if deleted_user.deleted_count > 0:
        logger.info("User deleted", user=deleted_user)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")
