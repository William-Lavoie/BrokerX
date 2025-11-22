from abc import abstractmethod
from decimal import Decimal
from typing import Optional
from uuid import UUID

from portfolio.domain.ports.portfolio_repository import PortfolioDTO


class PortfolioDAO:

    @abstractmethod
    def get_balance(self, client_id: UUID) -> PortfolioDTO:
        pass

    @abstractmethod
    def buy_holdings(
        self,
        client_id: UUID,
        symbol: str,
        name: str,
        quantity: int,
        buying_price: Decimal,
        current_price: Optional[Decimal] = None,
    ) -> PortfolioDTO:
        pass

    @abstractmethod
    def reserve_holdings(
        self, client_id: UUID, symbol: str, quantity: int
    ) -> PortfolioDTO:
        pass

    @abstractmethod
    def release_holdings(
        self, client_id: UUID, symbol: str, quantity: int
    ) -> PortfolioDTO:
        pass
