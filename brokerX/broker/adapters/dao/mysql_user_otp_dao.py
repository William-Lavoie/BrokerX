from abc import abstractmethod
from ...models import User, UserOPT

# TODO: error handling if user doesnt exist
class MySQLUserOTPDAO:
    def set_secret_key(self, email: str, secret: str) -> bool:
        db_user = User.objects.get(email=email)
        userOPT, created = UserOPT.objects.update_or_create(
            user=db_user, defaults={"secret": secret, "number_attempts": 0}
        )
        return True

    def get_secret_key(self, email: str) -> str:
        return UserOPT.objects.only("secret").get(user__email=email).secret

    def increment_attempts(self, email: str) -> bool:
        otp = UserOPT.objects.get(user__email=email)

        if otp.number_attempts >= 2:
            otp.delete()
            return False

        else:
            otp.number_attempts += 1
            otp.save()
            return True

    def delete_passcode(self, email: str) -> bool:
        UserOPT.objects.get(user__email=email).delete()
        return True
