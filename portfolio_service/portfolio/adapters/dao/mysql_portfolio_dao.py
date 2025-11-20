import logging
from decimal import Decimal
from uuid import UUID

from django.db import transaction

from portfolio.domain.ports.dao.portfolio_dao import PortfolioDAO, PortfolioDTO
from portfolio.models import Portfolio

logger = logging.getLogger("mysql")


class MySQLPortfolioDAO(PortfolioDAO):
    def get_balance(self, client_id: UUID) -> PortfolioDTO:
        portfolio, created = Portfolio.objects.get_or_create(client_id=client_id)

        holdings = [HoldingDTO(client_id=holding.client_id, symbol=holding.symbol) for holding in order.holdings]
 
        return PortfolioDTO(code=201 if created else 200, )


