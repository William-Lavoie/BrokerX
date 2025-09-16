from abc import abstractmethod

from ...domain.entities.user import User

class OTPRepository():
    @abstractmethod
    def send_passcode(self, email: str) -> None:
        pass

    @abstractmethod
    def verify_passcode(self, passcode: str, user: User) -> bool:
        pass
