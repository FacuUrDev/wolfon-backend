import io
from typing import List

from pandas import DataFrame

from src.application.services.card_service import CardService
from src.infrastructure import logger


class CardExportService:
    def __init__(self, card_service: CardService):
        self.card_service = card_service

    async def create_ticket(self, card_ids: List[str], vendor_data: dict = None):
        # WARNING: acá es posible que necesite un DTO para convertir la tarjeta a un ticket
        products = list(await self.card_service.get_card(card_ids))
        ticket_data = {"products": products, **vendor_data}
        logger.info("Creating ticket", products=products)
        return generate_ticket(ticket_data)


if __name__ == "__main__":
    import asyncio
    from src.infrastructure import get_database
    from src.infrastructure.repositories.mongo_card_repository import MongoCardInterface

    card_service = CardService(MongoCardInterface(get_database("wolfon_dev")))
    card_import_service = CardExportService(card_service)

    card_ids = [
        "688520351927a530cb24a104",
        "68854238c0eb386113cbd42e"
    ]
    from src.domain.static.tickets import generate_ticket

    # Example Usage:
    ticket_data = {
        'supermarket_name': 'Nombre del vendedor',
        'logo_url': 'https://placehold.co/150x50/ADD8E6/00008B?text=GROCER_LOGO',  # Example logo
        'vendor_address': '456 Oak Avenue, Springfield, USA',
        'vendor_phone': '+1 (987) 654-3210',
        'vendor_email': 'contact@mylocalgrocer.com',
        'receipt_no': 'REC-987654321',
        'products': [
            {'name': 'Organic Bananas', 'qty': 1.5, 'unit': 'kg', 'price': 2.99},
            {'name': 'Whole Wheat Bread', 'qty': 1, 'unit': 'loaf', 'price': 3.50},
            {'name': 'Canned Tomatoes', 'qty': 3, 'unit': 'can', 'price': 1.20},
            {'name': 'Ground Beef', 'qty': 0.75, 'unit': 'kg', 'price': 8.99},
            {'name': 'Fresh Spinach', 'qty': 1, 'unit': 'bunch', 'price': 2.00},
        ],
        'tax_rate': 0.07  # 7% tax
    }

    generated_html = generate_ticket(ticket_data)

    # You can now save this HTML to a file or serve it via a web application
    with open("supermarket_ticket.html", "w") as f:
        f.write(generated_html)
    print("HTML ticket generated and saved to supermarket_ticket.html")

    # If you want to print the HTML to console (for debugging/inspection)
    # print(generated_html)
