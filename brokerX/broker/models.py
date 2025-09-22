from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User

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
        max_length=20,
        choices=[("A", "Active"), ("P", "Pending"), ("R", "Rejected")]
    )


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.FloatField()


class ClientOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    secret = models.TextField(max_length=100)
    number_attempts = models.SmallIntegerField(
        default=0, validators=[MaxValueValidator(3)]
    )
