from django.db import models
from django.core.validators import MaxValueValidator

# The models will be accessed only through DAO, otherwise use entities
# i.e the model is only used to define the DB

# TODO: separate models into separate files
# TODO: add indexing to make faster queries


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    birth_date = models.DateField()
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20, choices=[("A", "Active"), ("P", "Pending"), ("R", "Rejected")]
    )


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.FloatField()


class UserOPT(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    secret = models.TextField(max_length=100)
    number_attempts = models.SmallIntegerField(
        default=0, validators=[MaxValueValidator(3)]
    )
