from django.db import models

# Create your models here.
class HistoricalPrices(models.Model):
    date = models.DateField()
    ticker = models.CharField(max_length=10)
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.DecimalField(max_digits=20, decimal_places=0)

    def __str__(self):
        return self.title
