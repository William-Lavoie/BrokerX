import uuid

from client.models import Client
from django.core.validators import MaxValueValidator
from django.db import models


class OTP(models.Model):
    client_id = models.UUIDField(db_index=True, editable=False, unique=True)
    secret = models.TextField(max_length=100)
    number_attempts = models.SmallIntegerField(
        default=0, validators=[MaxValueValidator(3)]
    )
