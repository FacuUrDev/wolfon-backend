from typing import List
from uuid import UUID

from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder

from src.domain.models import Card

router = APIRouter()


@router.post("/", response_description="Create a new card", status_code=status.HTTP_201_CREATED, response_model=Card)
def create_card(request: Request, card: Card = Body(...)):
    card = jsonable_encoder(card)
    new_card = request.app.database["cards"].insert_one(card)
    created_card = request.app.database["cards"].find_one(
        {"_id": new_card.inserted_id}
    )

    return created_card


@router.get("/{user_id}", response_description="List all cards", response_model=List[Card])
def list_cards(request: Request):
    cards = list(request.app.database["cards"].find({'user_id :user_id'}, limit=100))
    return cards


@router.get("/{id}", response_description="Get a single card by id", response_model=Card)
def find_card(id: str, request: Request):
    if (card := request.app.database["cards"].find_one({"_id": UUID(id)})) is not None:
        return card
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Card with ID {id} not found")


@router.put("/{id}", response_description="Update a card", response_model=Card)
def update_card(id: str, request: Request, card: Card = Body(...)):
    # card = {k: v for k, v in card.model_dump(exclude={'id'}).items() if v is not None}
    card = card.model_dump()
    if len(card) >= 1:
        update_result = request.app.database["cards"].update_one(
            {"_id": id}, {"$set": card}, upsert=True
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Card with ID {id} not found")

    if (
            existing_card := request.app.database["cards"].find_one({"_id": id})
    ) is not None:
        return existing_card

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Card with ID {id} not found")


@router.delete("/{id}", response_description="Delete a card")
def delete_card(id: str, request: Request, response: Response):
    delete_result = request.app.database["cards"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Card with ID {id} not found")
