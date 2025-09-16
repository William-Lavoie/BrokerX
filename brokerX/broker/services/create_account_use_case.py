from ..domain.entities.ports.account_repository import AccountRepository
from ..domain.entities.user import User
from ..services.commands.create_account_command import CreateAccountCommand

class CreateAccountUseCase:
    def __init__(self,  account_repository: AccountRepository):
        self.account_repository = account_repository

    def execute(self, command: CreateAccountCommand):

        # Create new Account entity
        account = User(first_name=command.first_name,
                       last_name=command.last_name,
                       address=command.address,
                       birth_date=command.birth_date,
                       email=command.email,
                       phone_number=command.phone_number,
                       status="pending"
        )

        # Save the new account
        self.account_repository.save(account)
