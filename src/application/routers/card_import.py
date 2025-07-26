import json
from typing import Any

from fastapi import APIRouter, UploadFile, File, Response, status, HTTPException

from src.application.routers.cards import card_service
from src.application.services.card_import_service import CardImportService
from src.infrastructure.logging.logger import logger

import_service = CardImportService(card_service)

router = APIRouter(
    prefix="/cards/import",
    tags=["card-imports"]
)


@router.post("/file", response_description="Upload cards from file", response_model=list[str])
async def import_cards_from_file(
        user_id: str,
        file: UploadFile = File(...)
):
    content = await file.read()
    try:
        imported_cards = await import_service.import_cards_from_file(content, user_id)
        return imported_cards
    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
