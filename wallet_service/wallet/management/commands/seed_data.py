from uuid import UUID

from django.core.management.base import BaseCommand
from wallet.models import Wallet


class Command(BaseCommand):
    help = "Seed the wallet service with mock data."

    def handle(self, *args, **options):
        self.stdout.write("Seeding wallet data...")

        wallets_data = [
            {
                "client_id": UUID("223e4567-e89b-12d3-a456-426614174001"),
                "balance": 10000.00,
            },  # Warren Buffet
            {
                "client_id": UUID("323e4567-e89b-12d3-a456-426614174002"),
                "balance": 8000.00,
            },  # John Bogle
            {
                "client_id": UUID("423e4567-e89b-12d3-a456-426614174003"),
                "balance": 5000.00,
            },  # Peter Lynch
        ]

        for wallet_data in wallets_data:
            client_id = wallet_data["client_id"]
            balance = wallet_data["balance"]

            # Ensure the wallet is only created if it doesn't already exist
            wallet, created = Wallet.objects.get_or_create(client_id=client_id)

            # Only update the balance if the wallet was created (or doesn't exist yet)
            if created:
                wallet.balance = balance
                wallet.save()

        self.stdout.write(self.style.SUCCESS("Wallet data seeded successfully."))
