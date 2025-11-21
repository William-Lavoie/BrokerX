import logging
from decimal import Decimal
from uuid import UUID

from django.db import transaction
from portfolio.domain.ports.dao.portfolio_dao import PortfolioDAO, PortfolioDTO
from portfolio.domain.ports.portfolio_repository import (HoldingDTO,
                                                         calculate_avg_price)
from portfolio.models import Holdings, Portfolio

logger = logging.getLogger("mysql")


class MySQLPortfolioDAO(PortfolioDAO):
    def get_portfolio(self, client_id: UUID) -> PortfolioDTO:
        portfolio, created = Portfolio.objects.get_or_create(client_id=client_id)

        holdings = [
            HoldingDTO(
                client_id=holding.client_id,
                symbol=holding.symbol,
                name=holding.name,
                quantity=holding.quantity,
                buying_price=holding.buying_price,
                current_price=holding.current_price,
                performance=holding.performance,
            )
            for holding in portfolio.holdings.all()
        ]

        return PortfolioDTO(
            code=201 if created else 200,
            client_id=client_id,
            value=portfolio.value,
            holdings=holdings,
            performance=portfolio.performance,
        )

    def set_holding(
        self,
        client_id: UUID,
        symbol: str,
        name: str,
        quantity: int,
        buying_price: Decimal,
    ):

        with transaction.atomic():
            portfolio = Portfolio.objects.get(client_id=client_id)

            holding, created = Holdings.objects.update_or_create(
                client_id=client_id,
                symbol=symbol,
                defaults={"name": name, "quantity": quantity},
            )

            if created:
                holding.buying_price = buying_price
            else:
                holding, buying_price = calculate_avg_price(
                    initial_quantity=holding.quantity - quantity,
                    new_quantity=quantity,
                    initial_price=holding.buying_price,
                    new_price=holding.buying_price,
                )
