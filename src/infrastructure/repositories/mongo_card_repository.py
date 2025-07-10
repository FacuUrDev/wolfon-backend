from bson.objectid import ObjectId

from src.domain.repositories.card_repository import CardRepository
from src.infrastructure.logging.logger import log


class MongoCardRepository(CardRepository):
    def __init__(self, db):
        self.db = db

    async def create(self, card):
        log.info('insert_one', card=card.model_dump())
        self.db.cards.insert_one(card.model_dump())
        return card.model_dump()

    async def find_by_id(self, card_id):
        return self.db.cards.find_one({"id": card_id})

    async def update(self, card):
        return self.db.cards.update_one({"id": card.id}, {"$set": card.model_dump(exclude={'_id'})})

    async def delete(self, card_id):
        return self.db.cards.delete_one({"id": card_id})
