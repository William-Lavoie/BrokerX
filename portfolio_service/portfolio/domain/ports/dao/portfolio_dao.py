from abc import abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from portfolio.adapters.result import Result
from portfolio.domain.entities.holding import Holding


@dataclass
class PortfolioDTO(Result):
    value: Decimal = Decimal("0.0")
    holdings: list[Holding] = []
    performance: Decimal = Decimal("0.0")


class PortfolioDAO:
    
    @abstractmethod
    def get_balance(self, client_id: UUID) -> PortfolioDTO:
        pass
