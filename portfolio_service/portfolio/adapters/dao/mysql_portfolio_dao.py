import logging
from uuid import UUID

from portfolio.domain.ports.dao.portfolio_dao import PortfolioDAO, PortfolioDTO
from portfolio.models import Portfolio
from portfolio.domain.ports.portfolio_repository import HoldingDTO

logger = logging.getLogger("mysql")


class MySQLPortfolioDAO(PortfolioDAO):
    def get_portfolio(self, client_id: UUID) -> PortfolioDTO:
        portfolio, created = Portfolio.objects.get_or_create(client_id=client_id)

        holdings = [HoldingDTO(client_id=holding.client_id, symbol=holding.symbol) for holding in portfolio.holdings.all()]
 
        return PortfolioDTO(code=201 if created else 200, client_id=client_id, value=portfolio.value, holdings=holdings, performance=portfolio.performance)


