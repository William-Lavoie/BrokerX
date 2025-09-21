from ...models import User

# TODO: add error handling in the case of a MySQL error
class MySQLUserDAO:
    def add_user(self, user: User):
        user, created = User.objects.get_or_create(
            email=user.email,
            defaults={
                "first_name": user.first_name,
                "last_name": user.last_name,
                "birth_date": user.birth_date,
                "phone_number": user.phone_number,
                "address": user.address,
                "status": user.status,
            },
        )

        if not created:
            print("There is already an account under this email")
            return False

        return True

    def update_status(self, email: str, new_status: str):
        user = User.objects.get(email=email)
        user.status = new_status
        user.save()
