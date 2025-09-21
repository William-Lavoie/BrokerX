from abc import abstractmethod
from ...models import User, UserOPT


class MySQLUserOTPDAO:
    def set_secret_key(self, user: User, secret: str) -> bool:
        db_user = User.objects.get(email=user.email)
        userOPT, created = UserOPT.objects.update_or_create(
            user=db_user, defaults={"secret": secret, "number_attempts": 0}
        )
        return True

    def get_secret_key(self, user: User) -> str:
        return UserOPT.objects.only("secret").get(user__email=user.email)

    def increment_attempts(self, user: User) -> bool:
        pass

    # TODO: use a database constraint instead?
    @abstractmethod
    def expire_passcode(self, user: User):
        """Expire a passcode after 3 attemps to prevent brute-forcing"""
        pass
