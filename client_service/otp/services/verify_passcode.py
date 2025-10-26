from ...domain.entities.client import ClientStatus
from ...domain.ports.client_repository import ClientRepository
from ...domain.ports.otp_repository import OTPRepository
from ...services.use_case_result import UseCaseResult


class VerifyPassCode:
    def __init__(
        self,
        otp_repository: OTPRepository,
        client_repository: ClientRepository,
    ):
        self.otp_repository = otp_repository
        self.client_repository = client_repository

    def execute(self, email: str, passcode: str) -> UseCaseResult:

        otp_dto = self.otp_repository.verify_passcode(email, passcode)

        if not otp_dto.success:
            if otp_dto.attempts >= 3:
                return UseCaseResult(
                    success=False,
                    message="You have made 3 attempts, the passcode has been disabled. You must ask for a new passcode.",
                    code=422,
                )
            return UseCaseResult(
                success=False,
                message=f"Wrong passcode. Attempts left : {3-otp_dto.attempts}",
                code=422,
            )

        result = self.client_repository.update_user_status(
            email, ClientStatus.ACTIVE.value
        )

        if not result.success:
            return UseCaseResult(
                success=False,
                message="There was an error, please try again.",
                code=500,
            )

        return UseCaseResult(
            success=True,
            message="You have entered the correct passcode",
            code=200,
        )

    def generate_passcode(self, email: str) -> UseCaseResult:
        otp_dto = self.otp_repository.create_passcode(email)

        if otp_dto.success:
            return UseCaseResult(
                success=True,
                message="The passcode was sent to your email",
                code=201,
            )

        else:
            return UseCaseResult(
                success=False,
                message="There was an error, please try again.",
                code=500,
            )
