from apscheduler.schedulers.blocking import BlockingScheduler
import yfinance as yf
from datetime import datetime
import numpy as np

# import models
from stock.models import StockRecord, StockInfo

'''
** find all objects
StockRecord.objects.all()
    return QuerySet

** find one type of objects
StockRecord.objects.filter(variable='value')
    return QuerySet

** find if object exists
StockRecord.objects.filter(variable='value').exists()
    return True or False
'''

RANKING_SIZE = 25

sched = BlockingScheduler({'apscheduler.timezone': 'Asia/Taipei'})

# every 2pm on weekdays
# Ranking Part
@sched.scheduled_job('cron', day_of_week='mon-fri', hour='14-15')
def getBuiltInRankings():
    stock_list = StockInfo.objects.all()
    list_size = len(stock_list)

    # check validity of data
    stock = stock_list[0]
    ticker = yf.Ticker(f'{stock.ticker}.TW')
    his = ticker.history(period='1d', actions=False)
    # valid
    if datetime.today().date() == his.index[0]:
        rise = np.zeros(list_size)
        fall = np.zeros(list_size)
        volume = np.zeros(list_size)

        for i in range(list_size):
            stock = stock_list[i]
            ticker = yf.Ticker(f'{stock.ticker}.TW')
            his = ticker.history(period='1d', actions=False)
            if his.empty:
                continue
            # rise, fall, volume
            rise[i] = (his['Close'][0] - his['Open'][0]) / his['Close'][0]
            fall[i] = -rise[i]
            volume[i] = his['Volume'][0]

        # sort
        top_rise = rise.argsort()[-RANKING_SIZE: ][ : : -1]
        top_fall = fall.argsort()[:RANKING_SIZE]
        top_volume = volume.argsort()[-RANKING_SIZE: ][ : : -1]

        # delete old records
        # consider deleting all of them?
        StockRecord.objects.filter(ranking_type='rise').delete()
        StockRecord.objects.filter(ranking_type='fall').delete()
        StockRecord.objects.filter(ranking_type='volume').delete()

        # store data into database
        # Model.objects.bulk_create([ Model(**{variable: value, ...}) for m in list ])
        StockRecord.objects.bulk_create([
            StockRecord(**{
                'ranking_type': 'rise',
                'stock_info': stock_list[ int(top_rise[i]) ],
                'ranking_number': i + 1,
                'last_modified': his.index[0]
            }) for i in range(RANKING_SIZE)
        ])
        StockRecord.objects.bulk_create([
            StockRecord(**{
                'ranking_type': 'fall',
                'stock_info': stock_list[ int(top_fall[i]) ],
                'ranking_number': i + 1,
                'last_modified': his.index[0]
            }) for i in range(RANKING_SIZE)
        ])
        StockRecord.objects.bulk_create([
            StockRecord(**{
                'ranking_type': 'volume',
                'stock_info': stock_list[ int(top_volume[i]) ],
                'ranking_number': i + 1,
                'last_modified': his.index[0]
            }) for i in range(RANKING_SIZE)
        ])

    # for stock in stock_list:
    #
    # ticker = yf.Ticker(f'{ticker}.TW')
    # his = ticker.history(period="__", interval="__", action=False)
    # value = abstract.Function(indicator_name, timeperiod=time_period)

# import
from django.core.management.base import BaseCommand

# Command class (the class name is fixed)
class Command(BaseCommand):
    help = 'for heroku run clock.py'

    # command method (the function name is fixed)
    def handle(self, *args, **options):
        sched.start()
