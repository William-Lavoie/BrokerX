from abc import abstractmethod
from typing import Optional

from ..entities.user import User


class UserRepository:
    @abstractmethod
    def add_user(self, user: User) -> None:
        pass

    @abstractmethod
    def update_user_status(self, email: str, new_status: str):
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        pass
