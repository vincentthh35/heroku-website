from django.contrib import admin

# Register your models here.
from .models import HistoricalPrices, StockInfo

admin.site.register(HistoricalPrices)
admin.site.register(StockInfo)
