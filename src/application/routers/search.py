from fastapi import APIRouter, HTTPException

from src.application.services.search_service import SearchService
from src.infrastructure import get_database

router = APIRouter()
search_service = SearchService(get_database())


@router.get("/")
async def search(collection: str, key: str, value: str):
    if collection not in search_service.db.list_collection_names():
        return HTTPException(status_code=404, detail=f"Collection {collection} not found")
    if key == '_id':
        value = str(value)
    results = search_service.find(collection, **{key: value})
    return results

# /search/cards?_id=687c17e5500c1817eb7344b8