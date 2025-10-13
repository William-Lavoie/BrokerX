# mypy: ignore-errors
import uuid

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# The models will be accessed only through DAO, otherwise use entities
# i.e the model is only used to define the DB

# TODO: separate models into separate files
# TODO: add indexing to make faster queries


class Client(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=100, unique=True)
    status = models.CharField(
        max_length=20, choices=[("A", "Active"), ("P", "Pending"), ("R", "Rejected")]
    )


class Wallet(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="wallets", null=True
    )
    balance = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0.00), MaxValueValidator(10000.00)],
    )


class ClientOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    secret = models.TextField(max_length=100)
    number_attempts = models.SmallIntegerField(
        default=0, validators=[MaxValueValidator(3)]
    )


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default="Unknown user")
    amount = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MaxValueValidator(0)]
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
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
    transaction_type = models.CharField(
        max_length=20, choices=[("D", "Deposit"), ("S", "Sale"), ("B", "Buy")]
    )
    message = models.CharField(max_length=300, blank=True)


class Stock(models.Model):
    symbol = models.CharField(max_length=10, db_index=True, unique=True)
    volume = models.IntegerField(validators=[MinValueValidator(1)])
    previous_close = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0.00), MaxValueValidator(10000.00)],
    )
    last_price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0.00), MaxValueValidator(10000.00)],
    )


class Order(models.Model):
    direction = models.CharField(max_length=100, choices=[("B", "Buy"), ("S", "Sell")])
    type = models.CharField(max_length=100, choices=[("M", "Market"), ("L", "Limit")])
    stock = models.ForeignKey(Stock, on_delete=models.SET_NULL, null=True)
    initial_quantity = models.IntegerField(validators=[MinValueValidator(1)])
    remaining_quantity = models.IntegerField(validators=[MinValueValidator(0)])
    limit = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0.00), MaxValueValidator(10000.00)],
        null=True,
    )
    duration = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
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
    related_orders = models.ManyToManyField("self")
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)


class Shares(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="shares")
    stock_symbol = models.CharField(max_length=50)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
