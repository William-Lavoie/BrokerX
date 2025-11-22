import logging
from decimal import Decimal
from typing import Optional
from uuid import UUID

from django.db import transaction
from portfolio.domain.ports.dao.portfolio_dao import PortfolioDAO, PortfolioDTO
from portfolio.domain.ports.portfolio_repository import (
    HoldingDTO,
    calculate_avg_price,
    calculate_holding_performance,
)
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
                reserved_for_sale=holding.reserved_for_sale,
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

    def buy_holdings(
        self,
        client_id: UUID,
        symbol: str,
        name: str,
        quantity: int,
        buying_price: Decimal,
        current_price: Optional[Decimal] = None,
    ) -> PortfolioDTO:
        try:
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
                    holding.buying_price = calculate_avg_price(
                        initial_quantity=holding.quantity - quantity,
                        new_quantity=quantity,
                        initial_price=holding.buying_price,
                        new_price=buying_price,
                    )

                if current_price:
                    holding.current_price = current_price

                elif holding.current_price is None:
                    holding.current_price = holding.buying_price

                holding.performance = calculate_holding_performance(
                    buying_price=holding.buying_price,
                    current_price=holding.current_price,
                )

                holding.save()

                portfolio.holdings.add(holding)

                total_value = sum(
                    h.current_price * h.quantity for h in portfolio.holdings.all()
                )

                portfolio.value = total_value
                portfolio.performance = (
                    sum(h.performance for h in portfolio.holdings.all())
                    / portfolio.holdings.count()
                    if portfolio.holdings.count() > 0
                    else Decimal("0.00")
                )
                portfolio.save()

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
                    code=200,
                    client_id=client_id,
                    value=portfolio.value,
                    holdings=holdings,
                    performance=portfolio.performance,
                )

        except Portfolio.DoesNotExist:
            logger.error(f"Portfolio for client_id {client_id} does not exist.")
            return PortfolioDTO(
                code=404,
                client_id=client_id,
            )
