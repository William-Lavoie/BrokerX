from uuid import UUID

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from order.models import Order


class Command(BaseCommand):
    help = "Seed the order service with mock data."

    def handle(self, *args, **options):
        self.stdout.write("Seeding order data...")

        orders = [
            {
                "order_id": UUID("523e4567-e89b-12d3-a456-426614174004"),
                "client_id": UUID("223e4567-e89b-12d3-a456-426614174001"),
                "stock_symbol": "AAPL",
                "quantity": 500,
                "order_type": "BUY",
                "order_style": "MARKET",
                "order_duration": "GTC",
                "price": 150.00,
                "status": "PENDING",
            },
            {
                "order_id": UUID("623e4567-e89b-12d3-a456-426614174005"),
                "client_id": UUID("223e4567-e89b-12d3-a456-426614174001"),
                "stock_symbol": "AAPL",
                "quantity": 100,
                "order_type": "SELL",
                "order_style": "MARKET",
                "order_duration": "GTC",
                "price": 150.00,
                "status": "PENDING",
            },
            {
                "order_id": UUID("623e4567-e89b-12d3-a456-426614174006"),
                "client_id": UUID("323e4567-e89b-12d3-a456-426614174002"),
                "stock_symbol": "MSFT",
                "quantity": 50,
                "order_type": "SELL",
                "order_style": "MARKET",
                "order_duration": "GTC",
                "price": 300.00,
                "status": "PENDING",
            },
            {
                "order_id": UUID("723e4567-e89b-12d3-a456-426614174006"),
                "client_id": UUID("423e4567-e89b-12d3-a456-426614174003"),
                "stock_symbol": "GOOGL",
                "quantity": 20,
                "order_type": "BUY",
                "order_style": "MARKET",
                "order_duration": "GTC",
                "price": 2800.00,
                "status": "PENDING",
            },
            {
                "order_id": UUID("823e4567-e89b-12d3-a456-426614174007"),
                "client_id": UUID("423e4567-e89b-12d3-a456-426614174003"),
                "stock_symbol": "TSLA",
                "quantity": 10,
                "order_type": "BUY",
                "order_style": "MARKET",
                "order_duration": "GTC",
                "price": 700.00,
                "status": "PENDING",
            },
        ]

        for order_data in orders:
            try:
                # Get or create the order
                Order.objects.get_or_create(
                    order_id=order_data["order_id"],
                    defaults=order_data,  # Use defaults to avoid overwriting order_id
                )
                self.stdout.write(
                    f"Order {order_data['order_id']} seeded successfully."
                )

            except IntegrityError as e:
                # Handle IntegrityError if duplicate entry exists
                self.stdout.write(
                    self.style.WARNING(
                        f"Order with ID {order_data['order_id']} already exists, skipping."
                    )
                )
                continue  # Skip to the next order if a duplicate is found

        self.stdout.write(self.style.SUCCESS("Order data seeded successfully."))
