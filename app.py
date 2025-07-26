from contextlib import asynccontextmanager

from fastapi import FastAPI
# from mangum import Mangum
from pymongo.mongo_client import MongoClient
from starlette.responses import RedirectResponse

from src import cards_router, users_router, card_import_router
from src.infrastructure.config.settings import Settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb_client = MongoClient(Settings().database_url)
    # app.database = app.mongodb_client['wolfon_dev']
    print("Connected to the MongoDB database!")
    yield
    app.mongodb_client.close()
    print("Disconnected from the MongoDB database!")


app = FastAPI(lifespan=lifespan)
app.include_router(cards_router)
app.include_router(card_import_router)
app.include_router(users_router)


# app.include_router(cards_router, tags=["cards"], prefix="/api/cards")
# app.include_router(users_router, tags=["users"], prefix="/api/users")
# app.include_router(search_router, tags=["search"], prefix="/api/search")


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')

# lambda_handler = Mangum(app, lifespan="off")
