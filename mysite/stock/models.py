from django.db import models

# Create your models here.
class HistoricalPrices(models.Model):
    date = models.DateField()
    stock_id = models.CharField(max_length=10)
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.DecimalField(max_digits=20, decimal_places=0)
