from ...models import User
from django.db.models import Q

# TODO: add error handling in the case of a MySQL error
class MySQLUserDAO:
    def add_user(self, user: User) -> bool:
        existing_user = User.objects.filter(
            Q(email=user.email) | Q(phone_number=user.phone_number)
        ).first()

        if existing_user:
            print("The email or the phone number is already in use.")
            return False

        User.objects.create(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone_number=user.phone_number,
            birth_date=user.birth_date,
            address=user.address,
            status=user.status,
        )

        return True

    def update_status(self, email: str, new_status: str):
        user = User.objects.get(email=email)
        user.status = new_status
        user.save()
