import logging
from uuid import UUID

from portfolio.domain.entities.portfolio import PortfolioInvalidException
from portfolio.domain.ports.portfolio_repository import PortfolioRepository

from portfolio_service.exceptions import DataAccessException
from portfolio_service.use_case_results import UseCaseResult

logger = logging.getLogger("portfolio")


class ReserveHoldingsUseCaseResult(UseCaseResult):
    def __init__(self, message: str, code: int):
        super().__init__(message=message, code=code)

    def to_dict(self):
        return super().to_dict()


class ReserveHoldingsUseCase:
    def __init__(
        self,
        portfolio_repository: PortfolioRepository,
    ):
        self.portfolio_repository = portfolio_repository

    def reserve_holdings(
        self, client_id: UUID, symbol: str, quantity: int
    ) -> ReserveHoldingsUseCaseResult:
        try:
            self.portfolio_repository.reserve_holdings(
                client_id=client_id, symbol=symbol, quantity=quantity
            )

            return ReserveHoldingsUseCaseResult(
                message=f"Successfully reserved holdings.",
                code=200,
            )

        except PortfolioInvalidException as portfolio_exception:
            logger.exception(portfolio_exception.log_message)
            return ReserveHoldingsUseCaseResult(
                message=portfolio_exception.user_message,
                code=portfolio_exception.error_code,
            )

        except DataAccessException as data_access_exception:
            logger.exception(
                f"DataAccessException in ReserveHoldingsUseCase for client {client_id}"
            )
            return ReserveHoldingsUseCaseResult(
                message=data_access_exception.user_message,
                code=data_access_exception.error_code,
            )

    def release_holdings(
        self, client_id: UUID, symbol: str, quantity: int
    ) -> ReserveHoldingsUseCaseResult:
        try:
            self.portfolio_repository.release_holdings(
                client_id=client_id, symbol=symbol, quantity=quantity
            )

            return ReserveHoldingsUseCaseResult(
                message=f"Successfully released holdings.",
                code=200,
            )

        except PortfolioInvalidException as portfolio_exception:
            logger.exception(portfolio_exception.log_message)
            return ReserveHoldingsUseCaseResult(
                message=portfolio_exception.user_message,
                code=portfolio_exception.error_code,
            )

        except DataAccessException as data_access_exception:
            logger.exception(
                f"DataAccessException in ReleaseHoldingsUseCase for client {client_id}"
            )
            return ReserveHoldingsUseCaseResult(
                message=data_access_exception.user_message,
                code=data_access_exception.error_code,
            )
