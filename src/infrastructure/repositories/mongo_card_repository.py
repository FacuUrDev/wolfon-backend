from bson.objectid import ObjectId

from src.domain.repositories.card_repository import CardRepository


class MongoCardRepository(CardRepository):
    def __init__(self, db):
        self.db = db

    async def create(self, card):
        self.db.cards.insert_one(card.model_dump())
        return card.model_dump()

    async def find_by_id(self, card_id):
        return self.db.cards.find_one({"_id": ObjectId(card_id)})

    async def update(self, card):
        return self.db.cards.update_one({"_id": ObjectId(card.id)}, {"$set": card.model_dump(exclude={'_id'})})

    async def delete(self, card_id):
        return self.db.cards.delete_one({"_id": ObjectId(card_id)})
