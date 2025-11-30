import logging

from portfolio.adapters.django_portfolio_repository import DjangoPortfolioRepository
from portfolio.domain.entities.portfolio import PortfolioInvalidException

from portfolio_service.exceptions import DataAccessException
from portfolio_service.use_case_results import UseCaseResult

logger = logging.getLogger("portfolio")


class ProcessExchangeUseCase:
    def __init__(
        self,
    ):
        self.portfolio_repository = DjangoPortfolioRepository()

    def process_acquisitions(self, orders_info: dict) -> UseCaseResult:
        try:
            self.portfolio_repository.process_acquisitions(orders_info=orders_info)

            return UseCaseResult(
                message=f"Successfully processed acquisitions.",
                code=200,
            )

        except PortfolioInvalidException as portfolio_exception:
            logger.exception(portfolio_exception.log_message)
            return UseCaseResult(
                message=portfolio_exception.user_message,
                code=portfolio_exception.error_code,
            )

        except DataAccessException as data_access_exception:
            logger.exception(f"DataAccessException in ProcessExchangeUseCase")
            return UseCaseResult(
                message=data_access_exception.user_message,
                code=data_access_exception.error_code,
            )

    def process_transfers(self, orders_info: dict) -> UseCaseResult:
        try:
            self.portfolio_repository.process_transfers(orders_info=orders_info)

            return UseCaseResult(
                message=f"Successfully processed transfers.",
                code=200,
            )

        except PortfolioInvalidException as portfolio_exception:
            logger.exception(portfolio_exception.log_message)
            return UseCaseResult(
                message=portfolio_exception.user_message,
                code=portfolio_exception.error_code,
            )

        except DataAccessException as data_access_exception:
            logger.exception(f"DataAccessException in ProcessExchangeUseCase")
            return UseCaseResult(
                message=data_access_exception.user_message,
                code=data_access_exception.error_code,
            )
