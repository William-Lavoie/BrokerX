# mypy: ignore-errors

import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Wallet(models.Model):
    client_id = models.UUIDField(editable=False, unique=True, db_index=True)
    balance = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0.00), MaxValueValidator(10000.00)],
    )


class Transaction(models.Model):
    client_id = models.UUIDField(editable=False, db_index=True)
    amount = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MaxValueValidator(0)]
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    idempotency_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("C", "Completed"),
            ("P", "Pending"),
            ("R", "Rejected"),
            ("F", "Failed"),
        ],
        default="P",
    )
    message = models.CharField(max_length=300, blank=True)
