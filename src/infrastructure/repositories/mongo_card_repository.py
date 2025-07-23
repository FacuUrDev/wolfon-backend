from datetime import datetime, UTC
from typing import Any

from src.application.interfaces.card_interface import CardInterface
from src.domain import Card
from bson import ObjectId

class MongoCardInterface(CardInterface):
    def __init__(self, db):
        self.db = db

    async def create(self, card: Any):
        if isinstance(card, Card):
            card = card.model_dump()
        card['created_at'] = datetime.now(UTC)
        insert_result = self.db.cards.insert_one(card)
        return insert_result.inserted_id

    async def find_by_id(self, card_id):
        return self.db.cards.find_one({"_id": ObjectId(card_id)})

    async def update(self, card: Any):
        if isinstance(card, Card):
            card = card.model_dump()
        card['updated_at'] = datetime.now(UTC)
        if '_id' not in card:
            raise KeyError(f'Expected "_id" key in card data. Received {card}')
        _id = card['_id']
        del card['_id']
        return self.db.cards.update_one({"_id": ObjectId(_id)}, {"$set": card})

    async def delete(self, card_id):
        return self.db.cards.delete_one({"_id": ObjectId(card_id)})
