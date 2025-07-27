from fasthtml.common import *
import datetime
# Custom CSS styles

css_styles = Style("""
    /* Custom styles for ticket-like appearance */
    body {
        font-family: 'Inter', sans-serif;
        background-color: #f3f4f6; /* Light gray background */
        display: flex;
        justify-content: center;
        align-items: flex-start; /* Align to top for longer tickets */
        min-height: 100vh;
        padding: 20px;
    }

    .ticket-container {
        width: 100%;
        max-width: 400px; /* Max width for a typical ticket */
        background-color: #ffffff;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        padding: 24px;
        box-sizing: border-box; /* Include padding in width */
    }

    .dashed-border {
        border-top: 1px dashed #d1d5db; /* Light gray dashed line */
        padding-top: 16px;
        margin-top: 16px;
    }

    /* Ensure table cells align properly */
    .product-table th, .product-table td {
        padding-top: 8px;
        padding-bottom: 8px;
        text-align: left;
    }

    .product-table th:nth-child(2),
    .product-table td:nth-child(2) {
        /* Amount column */
        text-align: center;
    }

    .product-table th:nth-child(4),
    .product-table td:nth-child(4) {
        /* Price column */
        text-align: right;
    }
""")

def generate_ticket(data):
    now = datetime.datetime.now()
    current_date = now.strftime("%B %d, %Y")
    current_time = now.strftime("%I:%M:%S %p")
    subtotal = sum(product['qty'] * product['price'] for product in data['products'])
    tax = subtotal * data['tax_rate']
    total = subtotal + tax

    # Generate product rows
    product_rows = []
    for product in data["products"]:
        row = Tr(
            Td(product['name'], cls="py-2"),
            Td(str(product['qty']), cls="py-2 text-center"),
            Td(product['unit'], cls="py-2"),
            Td(f"$ {product['qty'] * product['price']:.2f}", cls="py-2 text-right"),
            cls="border-b border-gray-100"
        )
        product_rows.append(row)

    # Build the complete HTML structure
    html_doc = Html(
        Head(
            Meta(charset="UTF-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            Title("Wolfon Ticket"),
            # Tailwind CSS CDN
            Script(src="https://cdn.tailwindcss.com"),
            css_styles
        ),
        Body(
            Div(
                # Logo Section
                Div(
                    Img(
                        src=data['logo_url'],
                        alt=f"{data['supermarket_name']} Logo",
                        cls="mx-auto w-36 h-auto rounded-md object-contain"
                    ),
                    H1(data['supermarket_name'], cls="text-2xl font-bold text-gray-800 mt-4"),
                    cls="text-center mb-6"
                ),

                # Vendor Data Section
                Div(
                    P(Strong("Dirección:", cls="text-gray-700"), f" {data['vendor_address']}", cls="mb-1"),
                    P(Strong("Teléfono:", cls="text-gray-700"), f" {data['vendor_phone']}", cls="mb-1"),
                    P(Strong("Email:", cls="text-gray-700"), f" {data['vendor_email']}", cls="mb-1"),
                    P(Strong("Fecha:", cls="text-gray-700"), f" {current_date}"),
                    P(Strong("Hora:", cls="text-gray-700"), f" {current_time}"),
                    P(Strong("Ticket Nro:", cls="text-gray-700"), f" {data['receipt_no']}"),
                    cls="text-sm text-gray-600 mb-6 border-b pb-4 border-gray-200"
                ),

                # Products Table
                Div(
                    Table(
                        Thead(
                            Tr(
                                Th("Nombre", cls="py-2 font-semibold"),
                                Th("Cantidad", cls="py-2 font-semibold text-center"),
                                Th("Unidad", cls="py-2 font-semibold"),
                                Th("Precio", cls="py-2 font-semibold text-right"),
                                cls="border-b border-gray-200"
                            )
                        ),
                        Tbody(*product_rows),
                        cls="w-full text-sm text-gray-700 product-table"
                    ),
                    cls="mb-6"
                ),

                # Total Section
                Div(
                    # Div(
                    #     Span("Subtotal:", cls="font-semibold text-base"),
                    #     Span(f"$ {subtotal:.2f}", cls="text-base"),
                    #     cls="flex justify-between items-center mb-2"
                    # ),
                    # Div(
                    #     Span(f"Tax ({data['tax_rate'] * 100:.0f}%):", cls="font-semibold text-base"),
                    #     Span(f"$ {tax:.2f}", cls="text-base"),
                    #     cls="flex justify-between items-center mb-2"
                    # ),
                    Div(
                        Span("TOTAL:"),
                        Span(f"$ {total:.2f}"),
                        cls="flex justify-between items-center text-lg font-bold mt-4"
                    ),
                    cls="dashed-border text-gray-800"
                ),

                # Thank You Message / Footer
                Div(
                    P("Gracias por su compra!", cls="mb-1"),
                    P("Vuelva pronto."),
                    cls="text-center text-gray-500 text-xs mt-8 pt-4 border-t border-gray-200"
                ),

                cls="ticket-container"
            ),
            cls="bg-gray-100 flex items-center justify-center min-h-screen p-4"
        ),
        lang="en"
    )

    return to_xml(html_doc)