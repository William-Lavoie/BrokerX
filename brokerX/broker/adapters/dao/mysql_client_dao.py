from ...domain.entities.client import ClientProfile
from django.contrib.auth.models import User
from ...models import Client
from django.db.models import Q

# TODO: add error handling in the case of a MySQL error
class MySQLClientDAO:
    def add_user(self, client: ClientProfile) -> bool:
        existing_user = Client.objects.filter(
            Q(user__email=client.email) | Q(phone_number=client.phone_number)
        ).first()

        if existing_user:
            print("The email or the phone number is already in use.")
            return False

        user = User.objects.create(
            first_name=client.first_name,
            last_name=client.last_name,
            email=client.email,
            username=client.email
        )

        Client.objects.create(user=user, phone_number=client.phone_number,
            birth_date=client.birth_date,
            address=client.address,
            status=client.status,)

        return True

    def update_status(self, email: str, new_status: str):
        client = Client.objects.get(user__email=email)
        client.status = new_status
        client.save()
