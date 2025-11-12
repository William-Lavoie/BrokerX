from django.db import models


class Stock(models.Model):
    # Metadata
    symbol = models.CharField(max_length=10, db_index=True, unique=True)
    name = models.CharField(max_length=100)
    exchange = models.CharField(max_length=100)
    currency = models.CharField(max_length=10, default="CAD")

    # Daily prices
    last_price = models.DecimalField(max_digits=12, decimal_places=2)
    open_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    high_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    low_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    close_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )

    # Top of book
    bid_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    bid_size = models.IntegerField(null=True, blank=True)
    ask_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    ask_size = models.IntegerField(null=True, blank=True)

    # Volume and timestamp
    volume = models.BigIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=True)
