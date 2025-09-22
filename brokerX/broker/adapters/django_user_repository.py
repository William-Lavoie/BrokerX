from typing import Optional

from ..adapters.dao.mysql_user_dao import MySQLUserDAO
from ..domain.ports.user_repository import UserRepository
from ..domain.entities.user import User


class DjangoUserRepository(UserRepository):
    def __init__(self, dao=None):
        super().__init__()
        self.dao = dao if dao is not None else MySQLUserDAO()

    def add_user(self, user: User) -> bool:
        return self.dao.add_user(user)

    def update_user_status(self, email: str, new_status: str):
        self.dao.update_status(email, new_status)

    def find_by_email(self, email: str) -> Optional[User]:
        pass
