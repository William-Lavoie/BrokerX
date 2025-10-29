# mypy: ignore-errors

import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)


class Client(models.Model):
    client_id = models.UUIDField(db_index=True, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100, primary_key=True, db_index=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=100, unique=True, db_index=True)
    status = models.CharField(
        max_length=20, choices=[("A", "Active"), ("P", "Pending"), ("R", "Rejected")]
    )
