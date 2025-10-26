# mypy: ignore-errors

from django.contrib.auth.models import User
from django.db import models


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100, primary_key=True, db_index=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=100, unique=True)
    status = models.CharField(
        max_length=20, choices=[("A", "Active"), ("P", "Pending"), ("R", "Rejected")]
    )
