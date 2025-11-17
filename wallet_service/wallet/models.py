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


class Withdrawal(models.Model):
    client_id = models.UUIDField(editable=False, db_index=True)
    amount = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MaxValueValidator(0)]
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    idempotency_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("COMPLETED", "Completed"),
            ("PENDING", "Pending"),
            ("REJECTED", "Rejected"),
            ("FAILED", "Failed"),
        ],
        default="PENDING",
    )
    message = models.CharField(max_length=300, blank=True)


class ReservedFunds(models.Model):
    client_id = models.UUIDField(editable=False, db_index=True)
    order_id = models.UUIDField(editable=False)
    amount = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint("client_id", "order_id", name="unique_reservation_per_order")
        ]



class WalletAudit(models.Model):
    ACTIONS = [
        ("CREATE_WITHDRAWAL", "Withdraw Funds"),
        ("UPDATE_WITHDRAWAL_STATUS", "Update Withdrawal Status"),
        ("RESERVE_FUNDS", "Reserve Funds"),
        ("RELEASE_FUNDS", "Release Funds"),
    ]
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, blank=True, null=True)
    withdrawal = models.ForeignKey(
        Withdrawal, on_delete=models.CASCADE, null=True, blank=True
    )
    reserved_funds = models.ForeignKey(
        ReservedFunds, on_delete=models.CASCADE, null=True, blank=True
    )
    action = models.CharField(max_length=50, choices=ACTIONS)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    metadata = models.JSONField(default=dict, blank=True)
