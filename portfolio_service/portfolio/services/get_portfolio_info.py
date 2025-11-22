import logging
from decimal import Decimal
from typing import Optional
from uuid import UUID

from portfolio.domain.entities.portfolio import Portfolio, PortfolioInvalidException
from portfolio.domain.ports.portfolio_repository import PortfolioRepository

from portfolio_service.exceptions import DataAccessException
from portfolio_service.use_case_results import UseCaseResult

logger = logging.getLogger("portfolio")


class GetPortfolioInfoUseCaseResult(UseCaseResult):
    def __init__(self, message: str, code: int, portfolio: Optional[Portfolio] = None):
        super().__init__(message=message, code=code)
        self.portfolio = portfolio

    def to_dict(self):
        dict = super().to_dict()
        if self.portfolio is not None:
            dict["portfolio"] = self.portfolio.to_dict()

        return dict


class GetPortfolioInfoUseCase:
    def __init__(
        self,
        portfolio_repository: PortfolioRepository,
    ):
        self.portfolio_repository = portfolio_repository

    def get_portofolio_info(self, client_id: UUID) -> GetPortfolioInfoUseCaseResult:
        try:
            portfolio: Portfolio = self.portfolio_repository.get_portfolio(
                client_id=client_id
            )

            return GetPortfolioInfoUseCaseResult(
                message=f"Successfully retrieved portfolio.",
                code=200,
                portfolio=portfolio,
            )

        except PortfolioInvalidException as stock_exception:
            logger.warning(
                f"PortfolioInvalidException in GetPortfolioInfoUseCaseResult for client {client_id}"
            )
            return GetPortfolioInfoUseCaseResult(
                message=stock_exception.user_message,
                code=stock_exception.error_code,
            )

        except DataAccessException as data_access_exception:
            return GetPortfolioInfoUseCaseResult(
                message=data_access_exception.user_message,
                code=data_access_exception.error_code,
            )

    def buy_holdings(
        self,
        client_id: UUID,
        symbol: str,
        name: str,
        quantity: int,
        buying_price: Decimal,
        current_price: Optional[Decimal] = None,
    ) -> GetPortfolioInfoUseCaseResult:
        try:
            portfolio = self.portfolio_repository.buy_holdings(
                client_id=client_id,
                symbol=symbol,
                name=name,
                quantity=quantity,
                buying_price=buying_price,
                current_price=current_price,
            )

            return GetPortfolioInfoUseCaseResult(
                message=f"Successfully updated holding {symbol} in portfolio.",
                code=200,
                portfolio=portfolio,
            )

        except PortfolioInvalidException as stock_exception:
            logger.warning(
                f"PortfolioInvalidException in SetHoldingUseCase for client {client_id}"
            )
            return GetPortfolioInfoUseCaseResult(
                message=stock_exception.user_message,
                code=stock_exception.error_code,
            )

        except DataAccessException as data_access_exception:
            return GetPortfolioInfoUseCaseResult(
                message=data_access_exception.user_message,
                code=data_access_exception.error_code,
            )
