from django.contrib.auth.models import User

from ...models import ClientOTP


# TODO: error handling if user doesnt exist
class MySQLClientOTPDAO:
    def set_secret_key(self, email: str, secret: str) -> bool:
        user = User.objects.get(email=email)
        clientOTP, created = ClientOTP.objects.update_or_create(
            user=user, defaults={"secret": secret, "number_attempts": 0}
        )
        return True

    def get_secret_key(self, email: str) -> str:
        return ClientOTP.objects.only("secret").get(user__email=email).secret

    def increment_attempts(self, email: str) -> bool:
        otp = ClientOTP.objects.get(user__email=email)

        if otp.number_attempts >= 2:
            otp.delete()
            return False

        else:
            otp.number_attempts += 1
            otp.save()
            return True

    def delete_passcode(self, email: str) -> bool:
        ClientOTP.objects.get(user__email=email).delete()
        return True
