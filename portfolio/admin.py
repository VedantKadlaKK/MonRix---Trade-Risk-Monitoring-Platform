from django.contrib import admin
from .models import Portfolio, Trade, MarketPrice

admin.site.register(Portfolio)
admin.site.register(Trade)
admin.site.register(MarketPrice)