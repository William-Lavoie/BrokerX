from typing import Optional

from ...adapters.result import Result
from ...domain.entities.client import Client, ClientInvalidException, ClientStatus
from ...domain.ports.client_repository import ClientRepository
from ...domain.ports.otp_repository import OTPDTO, OTPRepository
from ...exceptions import DataAccessException
from ...services.use_case_result import UseCaseResult
from ..commands.create_client_command import CreateClientCommand


class CreateClientUseCaseResult(UseCaseResult):
    def __init__(
        self, success: bool, message: str, code: int, client: Optional[dict] = None
    ):
        super().__init__(success=success, message=message, code=code)
        self.client: Optional[dict] = client

    def to_dict(self):
        dict = super().to_dict()
        if self.client is not None:
            dict.update(self.client)
        return dict


class CreateClientUseCase:
    def __init__(
        self, client_repository: ClientRepository, otp_repository: OTPRepository
    ):
        self.client_repository = client_repository
        self.otp_repository = otp_repository

    def execute(self, command: CreateClientCommand) -> UseCaseResult:

        # Create new Client entity
        client = Client(
            first_name=command.first_name,
            last_name=command.last_name,
            address=command.address,
            birth_date=command.birth_date,
            email=command.email,
            phone_number=command.phone_number,
            password=command.password,
            status=ClientStatus.PENDING.value,
        )

        # Save the new user
        result: Result = self.client_repository.add_user(client)

        if not result.success:
            if result.code == 409:
                return UseCaseResult(
                    success=False,
                    message="There is already a user with the same email and/or phone number",
                    code=result.code,
                )
            elif result.code == 500:
                return UseCaseResult(
                    success=False,
                    message="There was an unexpected error. Please try again or contact customer support.",
                    code=result.code,
                )

        otp_result: OTPDTO = self.otp_repository.create_passcode(client.email)

        if not otp_result.success:
            return UseCaseResult(
                success=False,
                message="There was an error creating your passcode.",
                code=result.code,
            )

        return UseCaseResult(
            success=True, message="The user was successfully created", code=result.code
        )

    def get_client_info(self, email: str):
        try:
            client = self.client_repository.get_client(email=email)
            return CreateClientUseCaseResult(
                success=True,
                message="The information was retrieved successfully.",
                code=200,
                client=client.to_dict(),
            )

        except ClientInvalidException as client_exception:
            return CreateClientUseCaseResult(
                success=False,
                message=client_exception.user_message,
                code=client_exception.error_code,
            )

        except DataAccessException as data_access_exception:
            return CreateClientUseCaseResult(
                success=False,
                message=data_access_exception.user_message,
                code=data_access_exception.error_code,
            )
