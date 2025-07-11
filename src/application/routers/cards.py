from fastapi import APIRouter, Body, Response, HTTPException, status

from src.application.services.card_service import CardService
from src.domain.models import Card
from src.infrastructure.dependencies.database import get_database
from src.infrastructure.logging.logger import log
from src.infrastructure.repositories.mongo_card_repository import MongoCardRepository

router = APIRouter()
card_service = CardService(MongoCardRepository(get_database()))


@router.post("/", response_description="Create a new card", status_code=status.HTTP_201_CREATED, response_model=Card)
async def create_card(card: Card):
    log.info("Creating new card", card=card)
    new_card = await card_service.create_card(card)
    return new_card


@router.get("/{card_id}", response_description="Get a single card by id", response_model=Card)
async def find_card(card_id: str):
    # return await card_service.get_card(card_id)
    if (card := await card_service.get_card(card_id)) is not None:
        card['_id'] = str(card['_id'])
        return card
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Card with ID {card_id} not found")


@router.put("/{id}", response_description="Update a card")
async def update_card(id: str, card: Card = Body(...)):
    founded_card = await card_service.update_card(id, card)
    if founded_card.modified_count > 0:
        log.info("Card updated successfully", card=founded_card)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Card with ID {id} not found")


@router.delete("/{id}", response_description="Delete a card")
async def delete_card(id: str):
    delete_card = await card_service.delete_card(id)
    if delete_card.deleted_count > 0:
        log.info("Card deleted successfully", card=delete_card)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Card with ID {id} not found")
