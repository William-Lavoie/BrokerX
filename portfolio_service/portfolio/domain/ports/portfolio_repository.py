from abc import abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from uuid import UUID

from portfolio.adapters.result import Result
from portfolio.domain.entities.portfolio import Portfolio
from portfolio.domain.entities.holding import Holding


@dataclass
class HoldingDTO(Result):
    code: int
    client_id: UUID
    symbol: str = ""
    name: str = ""
    quantity: int = 0
    buying_price: Optional[Decimal] = None,
    current_price: Optional[Decimal] = None,
    performance: Optional[Decimal] = None,


class PortfolioDTO(Result):
    def __init__(self, code: int, client_id: UUID,  value: Decimal = Decimal("0.00"), holdings: list[Holding] = [], performance: Decimal = Decimal("0.00")):
        super().__init__(code=code, client_id=client_id)
        self.value = value
        self.holdings = holdings
        self.performance = performance


class PortfolioRepository:
    @abstractmethod
    def get_portfolio(self, client_id: UUID) -> PortfolioDTO:
        pass


    def get_holding_from_dto(self, holding_dto) -> Holding:
        return Holding(
            client_id=holding_dto.client_id,
            symbol=holding_dto.symbol,
            name=holding_dto.name,
            buying_price=holding_dto.buying_price,
            current_price=holding_dto.current_price,
            performance=holding_dto.performance
        )
        
    def get_portfolio_from_dto(self, portfolio_dto) -> Portfolio:
        return Portfolio(
            client_id=portfolio_dto.client_id,
            value=portfolio_dto.value,
            performance=portfolio_dto.performance,
            holdings=[self.get_holding_from_dto(holding_dto) for holding_dto in portfolio_dto.holdings]
        )
    
