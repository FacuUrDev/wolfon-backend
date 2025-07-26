from fastapi import APIRouter, Body, Response, HTTPException, status

from src.application.services.card_service import CardService
from src.domain import Card
from src.infrastructure import get_database, logger
from src.infrastructure.repositories.mongo_card_repository import MongoCardInterface

router = APIRouter()
card_service = CardService(MongoCardInterface(get_database()))


@router.post("/", response_description="Create a new card", status_code=status.HTTP_201_CREATED, response_model=Card)
async def create_card(card: Card):
    # logger.info("Creating new card", card=card)
    await logger.ainfo("Creating new card", card=card)
    inserted_id = await card_service.create_card(card)
    card.id = str(inserted_id)
    return card


@router.get("/{card_id}", response_description="Get a single card by id", response_model=Card)
async def find_card(card_id: str):
    if (card := await card_service.get_card(card_id)) is not None:
        card['_id'] = str(card['_id'])
        return card
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Card with ID {card_id} not found")


@router.put("/", response_description="Update a card")
async def update_card(card=Body(...)):
    founded_card = await card_service.update_card(card)
    if founded_card.modified_count > 0:
        logger.info("Card updated successfully", card=founded_card)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Card with ID {id} not found")


@router.delete("/{card_id}", response_description="Delete a card")
async def delete_card(card_id: str):
    deleted_card = await card_service.delete_card(card_id)
    if deleted_card.deleted_count > 0:
        logger.info("Card deleted successfully", card=deleted_card)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Card with ID {id} not found")
