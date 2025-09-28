from ...adapters.result import Result
from ...domain.entities.client import ClientProfile, ClientStatus
from ...domain.ports.client_repository import ClientRepository
from ...domain.ports.otp_repository import OTPDTO, OTPRepository
from ...services.use_case_result import UseCaseResult
from ..commands.create_client_command import CreateClientCommand


class CreateClientUseCase:
    def __init__(
        self, client_repository: ClientRepository, otp_repository: OTPRepository
    ):
        self.client_repository = client_repository
        self.otp_repository = otp_repository

    def execute(self, command: CreateClientCommand) -> UseCaseResult:

        # Create new ClientProfile entity
        client = ClientProfile(
            first_name=command.first_name,
            last_name=command.last_name,
            address=command.address,
            birth_date=command.birth_date,
            email=command.email,
            phone_number=command.phone_number,
            password=command.password,
            status=ClientStatus.PENDING,
        )

        # Save the new user
        result: Result = self.client_repository.add_user(client)

        if not result.success:
            if result.code == 409:
                return UseCaseResult(
                    success=False,
                    message="There is already a user with the same email and/or phone number",
                )
            elif result.code == 500:
                return UseCaseResult(
                    success=False,
                    message="There was an unexpected error. Please try again or contact customer support.",
                )

        otp_result: OTPDTO = self.otp_repository.create_passcode(client)

        if not otp_result.success:
            return UseCaseResult(
                success=False,
                message="There was an error creating your passcode.",
            )

        return UseCaseResult(success=True, message="The user was successfully created")
