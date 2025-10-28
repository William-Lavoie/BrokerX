# mypy: ignore-errors

import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Order(models.Model):
    order_id = models.UUIDField(editable=False, primary_key=True)
    client_id = models.UUIDField(db_index=True)
    direction = models.CharField(max_length=1, choices=[("B", "Buy"), ("S", "Sell")])
    symbol = models.CharField(max_length=100, db_index=True, editable=False)
    initial_quantity = models.IntegerField(validators=[MinValueValidator(1)])
    remaining_quantity = models.IntegerField(validators=[MinValueValidator(0)])
    limit = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0.00), MaxValueValidator(10000.00)],
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    last_updated_at = models.DateTimeField(auto_now=True, db_index=True)
    status = models.CharField(
        max_length=1,
        choices=[
            ("C", "Completed"),
            ("P", "Pending"),
            ("R", "Rejected"),
            ("F", "Failed"),
        ],
        default="P",
    )
    related_orders = models.ManyToManyField("self")
