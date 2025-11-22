from decimal import Decimal
from typing import Optional
from uuid import UUID

from portfolio.adapters.dao.mysql_portfolio_dao import MySQLPortfolioDAO
from portfolio.domain.entities.portfolio import Portfolio
from portfolio.domain.ports.portfolio_repository import PortfolioRepository

from portfolio_service.exceptions import DataAccessException


class DjangoPortfolioRepository(PortfolioRepository):
    def __init__(self, dao=None, redis=None):
        super().__init__()
        self.dao = dao if dao is not None else MySQLPortfolioDAO()

    # self.redis = redis if redis is not None else RedisPortfolio()

    def get_portfolio(self, client_id: UUID) -> Portfolio:
        portfolio_dto = self.dao.get_portfolio(client_id=client_id)
        if not portfolio_dto.code:
            raise DataAccessException(
                user_message="An unexpected error occured while trying to fetch your portfolio."
            )

        # self.redis.set_wallet_balance(
        #    client_id=client_id, balance=wallet_dto.balance
        # )

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
