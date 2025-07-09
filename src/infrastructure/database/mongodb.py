from config import MongoCreds
from pymongo.mongo_client import MongoClient

class MongoDb:
    def __init__(self, db_name: str):
        self.client = MongoClient(MongoCreds().url)
        self.db = self.client[db_name]

    def close(self):
        self.client.close()

mongodb = MongoDb("wolfon_dev")

mongodb.db.cards.find_one({'_id':'5851b988-358d-4095-a71c-3fa04a61170f'})