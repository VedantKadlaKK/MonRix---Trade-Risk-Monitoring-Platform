from django.db import models
from django.contrib.auth.models import User


class Portfolio(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    risk_limit = models.DecimalField(
    max_digits=15,
    decimal_places=2,
    default=500000
)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Trade(models.Model):

    TRADE_TYPES = (
        ("BUY", "BUY"),
        ("SELL", "SELL"),
    )

    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name="trades"
    )

    symbol = models.CharField(max_length=20)

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    trade_type = models.CharField(
        max_length=10,
        choices=TRADE_TYPES
    )

    trade_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.trade_type} {self.symbol}"
    

class MarketPrice(models.Model):

    symbol = models.CharField(
        max_length=20,
        unique=True
    )

    current_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.symbol