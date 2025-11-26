from uuid import UUID
from django.core.management.base import BaseCommand

from client.models import Client, User

class Command(BaseCommand):
    help = "Seed the client service with mock data."

    def handle(self, *args, **options):
        self.stdout.write("Seeding client data...")

        user_warren, created = User.objects.get_or_create(
            username="warrenbuffett",
            email="warren.buffett@example.com",
            password="password123",
            first_name="Warren",
            last_name="Buffett",
        )

        Client.objects.get_or_create(
            client_id=UUID("223e4567-e89b-12d3-a456-426614174001"),
            user=user_warren,
            email="warren.buffett@example.com",
            first_name="Warren",
            last_name="Buffett",
            address="3555 Farnam St, Omaha, NE, USA",
            birth_date="1930-08-30",
            phone_number="+14025551234",
            status="ACTIVE",
        )

        user_bogle, created = User.objects.get_or_create(
            username="johnbogle",
            email="john.bogle@example.com",
            password="password123",
            first_name="John",
            last_name="Bogle",
        )

        Client.objects.get_or_create(
            client_id=UUID("323e4567-e89b-12d3-a456-426614174002"),
            user=user_bogle,
            email="john.bogle@example.com",
            first_name="John",
            last_name="Bogle",
            address="123 Vanguard Blvd, Malvern, PA, USA",
            birth_date="1929-05-08",
            phone_number="+14145551234",
            status="ACTIVE",
        )

        user_lynch, created = User.objects.get_or_create(
            username="peterlynch",
            email="peter.lynch@example.com",
            password="password123",
            first_name="Peter",
            last_name="Lynch",
        )

        Client.objects.get_or_create(
            client_id=UUID("423e4567-e89b-12d3-a456-426614174003"),
            user=user_lynch,
            email="peter.lynch@example.com",
            first_name="Peter",
            last_name="Lynch",
            address="1 Magellan St, Boston, MA, USA",
            birth_date="1944-01-19",
            phone_number="+16175551234",
            status="ACTIVE",
        )

        self.stdout.write(self.style.SUCCESS("Client data seeded successfully."))





