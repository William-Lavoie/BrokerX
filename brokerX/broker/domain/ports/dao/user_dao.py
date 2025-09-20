from abc import abstractmethod
from models import User


class UserDAO:

    # TODO: decouple the entities from the DAO
    @abstractmethod
    def add_user(self, user: User):
        pass

    @abstractmethod
    def update_status(self, user: User):
        pass
