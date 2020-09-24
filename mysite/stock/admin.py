from django.contrib import admin

# Register your models here.
from .models import HistoricalPrices, StockInfo, StockRecord

admin.site.register(HistoricalPrices)
admin.site.register(StockInfo)
admin.site.register(StockRecord)
