from typing import List, Any

from fastapi import APIRouter, Body, Request, Response, HTTPException, status

from src.application.services.user_service import UserService
from src.domain.models import User, Card
from src.infrastructure.dependencies.database import get_database
from src.infrastructure.logging.logger import log
from src.infrastructure.repositories.mongo_user_repository import MongoUserRepository

router = APIRouter()
user_service = UserService(MongoUserRepository(get_database()))


@router.post("/", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(user: User = Body(...)):
    if (user_created:=await user_service.create_user(user)) is not None:
        log.info("User created successfully", user=user_created)
        # user.id = str(user_created.inserted_id)
        return user
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")


@router.get("/list_cards/{user_id}", response_description="List cards for a user")
async def list_cards(user_id: str):
    log.info("Listing cards for user", user_id=user_id)
    if (cards := await user_service.list_cards(user_id)) is not None:
        cards_list = []
        for i, card in enumerate(cards):
            # card['_id'] = str(card['_id'])
            cards_list.append(card)
        return cards_list
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")

@router.get("/list", response_description="List all users")
async def list_users():
    users_list = await user_service.list_users()
    for i, user in enumerate(users_list):
        user['_id'] = str(user['_id'])
    return users_list
    # return await user_service.list_users()

@router.get("/{user_id}", response_description="Get a single user by id")
async def find_user(user_id: str):
    log.info("Finding user", user_id=user_id)
    user = await user_service.get_user(user_id)
    log.info("User found", user=user)
    if user is not None:
        # user['_id'] = user_id
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} not found")


@router.put("/{id}", response_description="Update a user")
async def update_user(id: str, user: User = Body(...)):
    updated_user = await user_service.update_user(id, user)
    if updated_user.modified_count > 0:
        log.info("User updated", user=updated_user)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")


@router.delete("/{id}", response_description="Delete a user")
async def delete_user(id: str):
    deleted_user = await user_service.delete_user(id)
    if deleted_user.deleted_count > 0:
        log.info("User deleted", user=deleted_user)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")
