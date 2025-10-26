from django.db import models
from django.core.validators import MaxValueValidator

from client.models import Client

class ClientOTP(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    secret = models.TextField(max_length=100)
    number_attempts = models.SmallIntegerField(
        default=0, validators=[MaxValueValidator(3)]
    )