import io
from time import perf_counter
from typing import List

import pandas as pd

from src.application.services.card_service import CardService
from src.domain.card_model import Card
from src.infrastructure import logger


class CardImportService:
    def __init__(self, card_service: CardService):
        self.card_service = card_service

    def _detect_file_type(self, file_content: bytes) -> str:
        # Check for Excel XLSX signature (PK zip format)
        if file_content.startswith(b'PK'):
            return 'xlsx'

        # Check for Excel XLS signature
        if file_content.startswith(b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1'):
            return 'xls'

        # Try to decode as UTF-8 text for CSV
        try:
            # Take first 1024 bytes for checking
            sample = file_content[:1024].decode('utf-8')
            # Check if it has common CSV characteristics
            if ',' in sample or ';' in sample:
                return 'csv'
        except UnicodeDecodeError:
            pass

        raise ValueError("Unsupported file format. Please provide CSV or Excel file.")

    def _read_file(self, file_content: bytes) -> pd.DataFrame:
        file_type = self._detect_file_type(file_content)

        if file_type in ['xlsx', 'xls']:
            return pd.read_excel(io.BytesIO(file_content))
        elif file_type == 'csv':
            # Try different CSV dialects
            return pd.read_csv(io.BytesIO(file_content))
            # try:
            #     pass
            # except:
            #     If comma doesn't work, try semicolon
            # return pd.read_csv(io.BytesIO(file_content), sep=';')

        raise ValueError("Unable to read file content")

    async def import_cards_from_file(self, file_content: bytes, user_id: str) -> List[str]:
        start_time = perf_counter()

        # Lee el archivo Excel
        df = self._read_file(file_content)
        read_time = perf_counter()
        logger.info("Importing cards from file", df=df.head(2))

        cards = []
        for _, row in df.iterrows():
            card = Card(
                **row,
                user_id=user_id,
            ).model_dump()
            cards.append(card)
        process_time = perf_counter()

        created_cards = await self.card_service.create_many_cards(cards)
        end_time = perf_counter()

        # Log timing information
        logger.info("Timing information",
                    file_read_time=f"{(read_time - start_time):.3f}s",
                    processing_time=f"{(process_time - read_time):.3f}s",
                    db_operation_time=f"{(end_time - process_time):.3f}s",
                    total_time=f"{(end_time - start_time):.3f}s")

        logger.info("Card created successfully", card=len(created_cards.inserted_ids))
        return [str(i) for i in created_cards.inserted_ids]


if __name__ == "__main__":
    import asyncio
    from src.infrastructure import get_database
    from src.infrastructure.repositories.mongo_card_repository import MongoCardInterface

    card_service = CardService(MongoCardInterface(get_database()))
    card_import_service = CardImportService(card_service)
    # asyncio.run(card_import_service.import_cards_from_excel(b'', '61337337-0000-4000-a002-000000000002'))
    with open('test_docs/test1.xlsx', 'rb') as file:
        creation_result = asyncio.run(
            card_import_service.import_cards_from_excel(file.read(), '68816e3b4c599bb6cf2de870'))
