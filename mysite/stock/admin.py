from django.contrib import admin

# Register your models here.
from .models import HistoricalPrices

admin.site.register(HistoricalPrices)
