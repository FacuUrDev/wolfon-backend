from bson.objectid import ObjectId, InvalidId
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult

from src.domain.repositories.card_repository import CardRepository
from src.infrastructure.logging.logger import log


class MongoCardRepository(CardRepository):
    def __init__(self, db):
        self.db = db

    async def create(self, card) -> dict:
        card_dict = card.model_dump()
        log.info('insert_one', card=card_dict)
        result: InsertOneResult = self.db.cards.insert_one(card_dict)
        # Si el modelo tiene un campo 'id', úsalo; si no, usa el ObjectId generado
        card_id = card_dict.get('id') or str(result.inserted_id)
        # find_by_id espera el campo 'id' personalizado, si existe, si no, busca por _id
        created_card = self.db.cards.find_one({"id": card_id}) or self.db.cards.find_one({"_id": result.inserted_id})
        if created_card:
            created_card['id'] = str(created_card.get('id', created_card.get('_id')))
        return created_card

    async def find_by_id(self, card_id: str) -> dict | None:
        # Primero intenta buscar por el campo 'id' personalizado
        document = self.db.cards.find_one({"id": card_id})
        if document:
            document["id"] = str(document.get("id", document.get("_id")))
            return document
        # Si no existe, intenta buscar por _id (ObjectId)
        try:
            object_id = ObjectId(card_id)
        except (InvalidId, TypeError):
            return None
        document = self.db.cards.find_one({"_id": object_id})
        if document:
            document["id"] = str(document.get("id", document.get("_id")))
        return document

    async def update(self, card) -> UpdateResult:
        card_dict = card.model_dump(exclude={'id'})
        return self.db.cards.update_one({"_id": ObjectId(card.id)}, {"$set": card_dict})

    async def delete(self, card_id: str) -> DeleteResult:
        return self.db.cards.delete_one({"_id": ObjectId(card_id)})
