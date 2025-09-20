from typing import Optional
from ..domain.ports.user_repository import UserRepository
from ..domain.entities.user import User


class DjangoUserRepository(UserRepository):
    def save(self, user: User) -> bool:
        pass


    def find_by_email(self, email: str) -> Optional[User]:
        pass
