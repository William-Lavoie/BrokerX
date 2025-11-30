from decimal import Decimal
from typing import Optional
from uuid import UUID

from portfolio.adapters.dao.mysql_portfolio_dao import MySQLPortfolioDAO
from portfolio.domain.entities.portfolio import Portfolio, PortfolioInvalidException
from portfolio.domain.ports.portfolio_repository import PortfolioRepository

from portfolio_service.exceptions import DataAccessException


class DjangoPortfolioRepository(PortfolioRepository):
    def __init__(self, dao=None, redis=None):
        super().__init__()
        self.dao = dao if dao is not None else MySQLPortfolioDAO()

    def get_portfolio(self, client_id: UUID) -> Portfolio:
        portfolio_dto = self.dao.get_portfolio(client_id=client_id)
        if not portfolio_dto.code:
            raise DataAccessException(
                user_message="An unexpected error occured while trying to fetch your portfolio."
            )

        return self.get_portfolio_from_dto(portfolio_dto)

    def buy_holdings(
        self,
        client_id: UUID,
        symbol: str,
        name: str,
        quantity: int,
        buying_price: Decimal,
        current_price: Optional[Decimal] = None,
    ) -> Portfolio:
        portfolio_dto = self.dao.buy_holdings(
            client_id=client_id,
            symbol=symbol,
            name=name,
            quantity=quantity,
            buying_price=buying_price,
            current_price=current_price,
        )

        if not portfolio_dto.success:
            raise DataAccessException(
                user_message="An unexpected error occured while trying to set your holding."
            )

        return self.get_portfolio_from_dto(portfolio_dto)

    def reserve_holdings(self, client_id: UUID, symbol: str, quantity: int) -> None:
        portfolio_dto = self.dao.reserve_holdings(
            client_id=client_id,
            symbol=symbol,
            quantity=quantity,
        )

        if portfolio_dto.code == 400:
            raise PortfolioInvalidException(
                user_message="Not enough holdings available to reserve the requested quantity.",
                log_message=(
                    f"Not enough holdings to reserve for client_id {client_id}."
                ),
                error_code=400,
            )

        elif portfolio_dto.code == 404:
            raise PortfolioInvalidException(
                user_message="The specified holding does not exist in the portfolio.",
                log_message=(
                    f"Holding {symbol} does not exist for client_id {client_id}."
                ),
                error_code=404,
            )

        elif not portfolio_dto.success:
            raise DataAccessException(
                user_message="An unexpected error occured while trying to reserve your holdings."
            )

    def release_holdings(self, client_id: UUID, symbol: str, quantity: int) -> None:
        portfolio_dto = self.dao.release_holdings(
            client_id=client_id,
            symbol=symbol,
            quantity=quantity,
        )

        if portfolio_dto.code == 400:
            raise PortfolioInvalidException(
                user_message="Not enough reserved holdings to release the requested quantity.",
                log_message=(
                    f"Not enough reserved holdings to release for client_id {client_id}."
                ),
                error_code=400,
            )

        elif portfolio_dto.code == 404:
            raise PortfolioInvalidException(
                user_message="The specified holding does not exist in the portfolio.",
                log_message=(
                    f"Holding {symbol} does not exist for client_id {client_id}."
                ),
                error_code=404,
            )

        elif not portfolio_dto.success:
            raise DataAccessException(
                user_message="An unexpected error occured while trying to release your holdings."
            )

    def process_acquisitions(self, orders_info: dict) -> None:

        for order in orders_info:
            client_id = order.get("client_id")
            symbol = order.get("symbol")
            quantity = order.get("quantity")
            buying_price = order.get("buying_price")
            name = order.get("name")
            current_price = order.get("current_price")

            portfolio_dto = self.dao.buy_holdings(
                client_id=client_id,
                symbol=symbol,
                name=name,
                quantity=quantity,
                buying_price=buying_price,
                current_price=current_price,
            )

            if not portfolio_dto.success:
                raise DataAccessException(
                    user_message="An unexpected error occured while trying to process your acquisitions."
                )

    def process_transfers(self, orders_info: list[dict]) -> None:
        for order in orders_info:
            client_id = order.get("client_id")
            symbol = order.get("symbol")
            quantity = order.get("quantity")

            portfolio_dto = self.dao.sell_holdings(
                client_id=client_id,
                symbol=symbol,
                quantity=quantity,
            )

            if not portfolio_dto.success:
                raise DataAccessException(
                    user_message="An unexpected error occured while trying to process your transfers."
                )
