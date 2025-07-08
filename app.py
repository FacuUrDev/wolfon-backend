from contextlib import asynccontextmanager

from fastapi import FastAPI
from pymongo.mongo_client import MongoClient

from config import MongoCreds
from src import cards_router, users_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb_client = MongoClient(MongoCreds().url)
    app.database = app.mongodb_client['wolfon_dev']
    print("Connected to the MongoDB database!")
    yield
    app.mongodb_client.close()
    print("Disconnected from the MongoDB database!")


app = FastAPI(lifespan=lifespan)
app.include_router(cards_router, tags=["cards"], prefix="/card")
app.include_router(users_router, tags=["users"], prefix="/user")
