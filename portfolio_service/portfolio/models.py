# mypy: ignore-errors

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.manager import RelatedManager


class Portfolio(models.Model):
    client_id = models.UUIDField(db_index=True, unique=True)
    value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0.00)],
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    performance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    holdings: RelatedManager["Holdings"]


class Holdings(models.Model):
    client_id = models.UUIDField(db_index=True)
    portfolio = models.ForeignKey(
        Portfolio, on_delete=models.CASCADE, related_name="holdings"
    )
    symbol = models.CharField(max_length=100, editable=False)
    name = models.CharField(max_length=100, editable=False)
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    buying_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
    )
    current_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
    )
    performance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    reserved_for_sale = models.IntegerField(
        default=0, validators=[MinValueValidator(0)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                "client_id", "symbol", name="unique_symbol_per_client"
            )
        ]
