from django.db import models

# Create your models here.
class StockInfo(models.Model):
    ticker = models.CharField(max_length=10, verbose_name='股票代號')
    stock_name = models.CharField(max_length=20, verbose_name='股票名稱')
    sector = models.CharField(max_length=30, verbose_name='行業別')

    def __str__(self):
        return f'{self.ticker} {self.stock_name}'

class HistoricalPrices(models.Model):
    date = models.DateField()
    stock_info = models.ForeignKey(StockInfo, on_delete=models.CASCADE)
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.DecimalField(max_digits=20, decimal_places=0)

    def __str__(self):
        return f'{self.date}: {self.ticker}'
