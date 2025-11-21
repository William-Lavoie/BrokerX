from abc import abstractmethod
from uuid import UUID

from portfolio.domain.ports.portfolio_repository import PortfolioDTO


class PortfolioDAO:

    @abstractmethod
    def get_balance(self, client_id: UUID) -> PortfolioDTO:
        pass
