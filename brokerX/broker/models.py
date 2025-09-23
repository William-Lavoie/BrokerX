import uuid
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.forms import ValidationError

# The models will be accessed only through DAO, otherwise use entities
# i.e the model is only used to define the DB

# TODO: separate models into separate files
# TODO: add indexing to make faster queries


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=100, primary_key=True)
    status = models.CharField(
        max_length=20, choices=[("A", "Active"), ("P", "Pending"), ("R", "Rejected")]
    )


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
    idempotency_key = models.UUIDField(default=uuid.uuid4, editable=False)
    status = (
        models.CharField(
            max_length=20,
            choices=[
                ("C", "Completed"),
                ("P", "Pending"),
                ("R", "Rejected"),
                ("F", "Failed"),
            ],
        ),
    )
    type = (
        models.CharField(
            max_length=20, choices=[("D", "Deposit"), ("S", "Sale"), ("B", "Buy")]
        ),
    )

    def save(self, *args, **kwargs):
        if self.pk:
            raise ValidationError(
                "Transactions cannot be edited. Please make a new one"
            )
        super().save(*args, **kwargs)
