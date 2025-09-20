from typing import Optional

from ..adapters.dao.mysql_user_dao import MySQLUserDAO
from ..domain.ports.user_repository import UserRepository
from ..domain.entities.user import User


class DjangoUserRepository(UserRepository):
    def __init__(self):
        super().__init__()
        self.dao = MySQLUserDAO()

    def add_user(self, user: User) -> bool:
        return self.dao.add_user(user)

    def find_by_email(self, email: str) -> Optional[User]:
        pass
