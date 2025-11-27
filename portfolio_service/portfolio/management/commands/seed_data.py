from uuid import UUID

from django.core.management.base import BaseCommand
from portfolio.models import Holdings, Portfolio


class Command(BaseCommand):
    help = "Seed the portfolio service with mock data."

    def handle(self, *args, **options):
        self.stdout.write("Seeding portfolio data...")

        # Warren Buffet
        portfolio_warren = Portfolio.objects.get_or_create(
            client_id=UUID("223e4567-e89b-12d3-a456-426614174001"),
            value=1500000.00,
            performance=0.12,
        )
        Holdings.objects.get_or_create(
            client_id=UUID("223e4567-e89b-12d3-a456-426614174001"),
            portfolio=portfolio_warren[0],
            symbol="AAPL",
            name="Apple Inc.",
            quantity=5000,
            buying_price=120.00,
            current_price=150.00,
            performance=0.25,
            reserved_for_sale=1000,
        )
        Holdings.objects.get_or_create(
            client_id=UUID("223e4567-e89b-12d3-a456-426614174001"),
            portfolio=portfolio_warren[0],
            symbol="BRK.B",
            name="Berkshire Hathaway Inc.",
            quantity=2000,
            buying_price=250.00,
            current_price=280.00,
            performance=0.12,
            reserved_for_sale=500,
        )
        Holdings.objects.get_or_create(
            client_id=UUID("223e4567-e89b-12d3-a456-426614174001"),
            portfolio=portfolio_warren[0],
            symbol="VEQT",
            name="Vanguard FTSE Global All Cap ex Canada Equity Index ETF",
            quantity=10000,
            buying_price=55.00,
            current_price=60.00,
            performance=0.09,
            reserved_for_sale=2000,
        )

        # John Bogle
        portfolio_bogle = Portfolio.objects.get_or_create(
            client_id=UUID("323e4567-e89b-12d3-a456-426614174002"),
            value=800000.00,
            performance=0.08,
        )
        Holdings.objects.get_or_create(
            client_id=UUID("323e4567-e89b-12d3-a456-426614174002"),
            portfolio=portfolio_bogle[0],
            symbol="XEQT",
            name="iShares Core Equity ETF Portfolio",
            quantity=8000,
            buying_price=48.00,
            current_price=50.00,
            performance=0.05,
            reserved_for_sale=1500,
        )
        Holdings.objects.get_or_create(
            client_id=UUID("323e4567-e89b-12d3-a456-426614174002"),
            portfolio=portfolio_bogle[0],
            symbol="MSFT",
            name="Microsoft Corporation",
            quantity=3000,
            buying_price=280.00,
            current_price=300.00,
            performance=0.07,
            reserved_for_sale=800,
        )
        Holdings.objects.get_or_create(
            client_id=UUID("323e4567-e89b-12d3-a456-426614174002"),
            portfolio=portfolio_bogle[0],
            symbol="AMZN",
            name="Amazon.com, Inc.",
            quantity=1000,
            buying_price=3400.00,
            current_price=3500.00,
            performance=0.03,
            reserved_for_sale=200,
        )

        # Peter Lynch
        portfolio_lynch = Portfolio.objects.get_or_create(
            client_id=UUID("423e4567-e89b-12d3-a456-426614174003"),
            value=600000.00,
            performance=0.10,
        )
        Holdings.objects.get_or_create(
            client_id=UUID("423e4567-e89b-12d3-a456-426614174003"),
            portfolio=portfolio_lynch[0],
            symbol="GOOGL",
            name="Alphabet Inc.",
            quantity=1500,
            buying_price=2700.00,
            current_price=2800.00,
            performance=0.04,
            reserved_for_sale=300,
        )
        Holdings.objects.get_or_create(
            client_id=UUID("423e4567-e89b-12d3-a456-426614174003"),
            portfolio=portfolio_lynch[0],
            symbol="TSLA",
            name="Tesla, Inc.",
            quantity=800,
            buying_price=680.00,
            current_price=700.00,
            performance=0.03,
            reserved_for_sale=150,
        )
        Holdings.objects.get_or_create(
            client_id=UUID("423e4567-e89b-12d3-a456-426614174003"),
            portfolio=portfolio_lynch[0],
            symbol="NVDA",
            name="NVIDIA Corporation",
            quantity=1200,
            buying_price=210.00,
            current_price=220.00,
            performance=0.06,
            reserved_for_sale=250,
        )

        self.stdout.write(self.style.SUCCESS("Portfolio data seeded successfully."))
