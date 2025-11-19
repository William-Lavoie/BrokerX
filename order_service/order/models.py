# mypy: ignore-errors

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class Order(models.Model):
    order_id = models.UUIDField(editable=False, primary_key=True)
    client_id = models.UUIDField(db_index=True)
    stock_symbol = models.CharField(max_length=100, db_index=True, editable=False)
    order_type = models.CharField(
        max_length=10, choices=[("BUY", "Buy"), ("SELL", "Sell")]
    )
    order_style = models.CharField(
        max_length=10, choices=[("MARKET", "Market"), ("LIMIT", "Limit")]
    )
    order_duration = models.CharField(
        max_length=10,
        choices=[
            ("GTC", "Good Till Cancelled"),
            ("IOC", "Immediate Or Cancel"),
            ("DAY", "Day"),
            ("GTD", "Good Till Date"),
            ("FOK", "Fill Or Kill"),
        ],
        default="GTC",
    )
    order_end_date = models.DateField(null=True, blank=True)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    quantity_executed = models.IntegerField(
        default=0, validators=[MinValueValidator(0)]
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    executed_at = models.DateTimeField(db_index=True, null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ("EXECUTED", "Executed"),
            ("PARTIALLY_EXECUTED", "Partially Executed"),
            ("PENDING", "Pending"),
            ("REJECTED", "Rejected"),
            ("FAILED", "Failed"),
        ],
        default="PENDING",
    )

    def clean(self):
        super().clean()
        if self.order_style == "LIMIT" and (self.price is None or self.price <= 0):
            raise ValidationError(
                "LIMIT orders must have a valid price greater than 0."
            )
        if self.quantity_executed > self.quantity:
            raise ValidationError("Quantity executed cannot exceed total quantity.")
        if self.order_duration == "GTD" and self.order_end_date is None:
            raise ValidationError("GTD orders must have an end date specified.")
        if self.order_duration != "GTD" and self.order_end_date is not None:
            raise ValidationError("Only GTD orders can have an end date specified.")


class OrderExecution(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="executions"
    )
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=12, decimal_places=2)
    executed_at = models.DateTimeField(auto_now_add=True, editable=False)
    buyer_client_id = models.UUIDField()
    seller_client_id = models.UUIDField()


class OrderAudit(models.Model):
    ACTIONS = [
        ("ORDER_PLACED", "Order Placed"),
        ("ORDER_EXECUTED", "Order Executed"),
        ("ORDER_PARTIALLY_EXECUTED", "Order Partially Executed"),
        ("ORDER_REJECTED", "Order Rejected"),
        ("ORDER_FAILED", "Order Failed"),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="audits")
    action = models.CharField(max_length=30, choices=ACTIONS)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)
