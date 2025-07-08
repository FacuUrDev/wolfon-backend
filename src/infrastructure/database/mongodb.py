from config import MongoCreds
from pymongo.mongo_client import MongoClient

class MongoDb:
    def __init__(self, db_name: str):
        self.client = MongoClient(MongoCreds().url)
        self.db = self.client[db_name]

    def close(self):
        self.client.close()
