from pymongo import MongoClient

from src.infrastructure.config.settings import settings


class DatabaseManager:
    client: MongoClient = MongoClient(settings.database_url)
    database = None


db_manager = DatabaseManager()


def get_database(database_name=settings.database_name):
    return db_manager.client[database_name]


def get_card_repository():
    from src.infrastructure.repositories.mongo_card_repository import MongoCardInterface
    return MongoCardInterface(get_database())


def get_user_repository():
    from src.infrastructure.repositories.mongo_user_repository import MongoUserInterface
    return MongoUserInterface(get_database())
