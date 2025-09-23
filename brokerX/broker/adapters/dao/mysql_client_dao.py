from django.contrib.auth.models import User
from django.db.models import Q

from ...domain.entities.client import ClientProfile
from ...models import Client


# TODO: add error handling in the case of a MySQL error
class MySQLClientDAO:
    def add_user(self, client: ClientProfile) -> bool:
        existing_user = Client.objects.filter(
            Q(user__email=client.email) | Q(phone_number=client.phone_number)
        ).first()

        if existing_user:
            print("The email or the phone number is already in use.")
            return False

        user = User.objects.create_user(  # type: ignore[attr-defined]
            first_name=client.first_name,
            last_name=client.last_name,
            email=client.email,
            username=client.email,
            password=client.password,
        )

        Client.objects.create(
            user=user,
            phone_number=client.phone_number,
            birth_date=client.birth_date,
            address=client.address,
            status=client.status,
        )

        return True

    def update_status(self, email: str, new_status: str):
        client = Client.objects.get(user__email=email)
        client.status = new_status
        client.save()

    def get_status(self, email: str) -> str:
        return Client.objects.only("status").get(user__email=email).status
