from typing import Optional
from ..domain.entities.ports.account_repository import AccountRepository
from ..domain.entities.user import User


class TestAccountRepository(AccountRepository):
    def save(self, account: User) -> None:
        print("Wow!")
        print(account.to_dict())

    def find_by_email(self, email: str) -> Optional[User]:
        pass
