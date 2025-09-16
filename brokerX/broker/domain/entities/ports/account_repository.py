from abc import abstractmethod
from typing import Optional

from ....domain.entities.user import User


class AccountRepository():
    @abstractmethod
    def save(self, account: User) -> None:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        pass
