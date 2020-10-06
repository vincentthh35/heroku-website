from django.db import models

# Create your models here.
class StockInfo(models.Model):
    ticker = models.CharField(max_length=10, verbose_name='股票代號')
    stock_name = models.CharField(max_length=20, verbose_name='股票名稱')
    sector = models.CharField(max_length=30, verbose_name='行業別')

    def __str__(self):
        return f'{self.ticker} {self.stock_name}'

# for built-in ranking methods and built-in filter methods
class StockRecord(models.Model):
    record_type = models.CharField(max_length=15, verbose_name='排行種類')
    title_dict = {
        'rise': '漲幅排行',
        'fall': '跌幅排行',
        'volume': '成交量排行',
    }
    remark_dict = {
        'rise': '漲幅',
        'fall': '跌幅',
        'volume': '成交量'
    }
    stock_info = models.ForeignKey(StockInfo, on_delete=models.CASCADE)
    # filter methods don't need this field
    ranking_number = models.DecimalField(max_digits=3, decimal_places=0, verbose_name='名次', blank=True)
    remark = models.CharField(max_length=10, blank=True)
    last_modified = models.DateField(null=True, verbose_name='紀錄日期')

    def __str__(self):
        if self.ranking_number is None:
            return f'[{self.record_type}]: {self.stock_info.ticker} {self.stock_info.stock_name}'
        else:
            return f'[{self.record_type}] #{self.ranking_number}: {self.stock_info.ticker} {self.stock_info.stock_name}'

# (currently of no use)
# for storing historical prices
class HistoricalPrices(models.Model):
    date = models.DateField(verbose_name='日期')
    stock_info = models.ForeignKey(StockInfo, on_delete=models.CASCADE)
    open = models.FloatField(verbose_name='開盤價')
    high = models.FloatField(verbose_name='(當日)最高價')
    low = models.FloatField(verbose_name='(當日)最低價')
    close = models.FloatField(verbose_name='收盤價')
    volume = models.DecimalField(max_digits=20, decimal_places=0, verbose_name='交易量')

    def __str__(self):
        return f'{self.date}: {self.stock_info.ticker}'
