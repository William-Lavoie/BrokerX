from decimal import Decimal
from uuid import UUID

from portfolio.domain.entities.holding import Holding


class PortfolioInvalidException(Exception):

    def __init__(
        self,
        user_message: str = "The portfolio is invalid.",
        log_message: str = "The portfolio is invalid.",
        error_code: int = 400,
    ):
        super().__init__(user_message)
        self.user_message = user_message
        self.log_message = log_message
        self.error_code = error_code


class Portfolio:

    def __init__(
        self,
        client_id: UUID,
        value: Decimal = Decimal("0.00"),
        performance: Decimal = Decimal("0.00"),
        holdings: list[Holding] = [],
    ):
        self.client_id = client_id
        self.value = value
        self.performance = performance
        self.holdings = holdings

        if value < 0:
            raise PortfolioInvalidException(
                user_message="Your portfolio cannot have a negative value",
                log_message="The value of the portfolio for client {client_id} was {value}",
                error_code=400,
            )

    def to_dict(self):
        return {
            "client_id": str(self.client_id),
            "value": Decimal(self.value) if self.value is not None else None,
            "performance": (
                Decimal(self.performance) if self.performance is not None else None
            ),
            "holdings": [holding.to_dict() for holding in self.holdings],
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            client_id=UUID(data["client_id"]),
            value=Decimal(data["value"]) if data.get("value") is not None else None,
            performance=(
                Decimal(data["performance"])
                if data.get("performance") is not None
                else None
            ),
            holdings=[Holding().from_dict(holding) for holding in data["holdings"]],
        )
