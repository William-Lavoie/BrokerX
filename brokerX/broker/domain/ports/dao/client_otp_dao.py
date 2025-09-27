from abc import abstractmethod

from ....adapters.result import Result


class ClientOTPDAO:
    @abstractmethod
    def set_secret_key(self, email: str, secret: str) -> Result:
        pass

    @abstractmethod
    def get_secret_key(self, email: str) -> Result:
        pass

    # TODO: use a database constraint instead?
    @abstractmethod
    def delete_passcode(self, email: str) -> Result:
        """Expire a passcode after 3 attemps, 10 mins or upon validation to prevent brute-forcing"""
        pass

    @abstractmethod
    def increment_attempts(self, email: str) -> Result:
        pass
