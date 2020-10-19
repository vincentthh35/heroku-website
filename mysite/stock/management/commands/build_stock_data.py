import requests
import pandas as pd
import yfinance as yf
import os
from django.core.management.base import BaseCommand
from stock.models import StockInfo, HistoricalPrices

class Command(BaseCommand):
    help = 'build the historical data of stock(s)'

    def saveDf(self, df, stock_info):
        # input: columns['index(Date)', 'High', 'Low', 'Open', 'Close', 'Volume']
        self.stdout.write(self.style.NOTICE(f'***** Begin processing {stock_info.ticker}.TW *****'))
        # parse through everything in df
        for index, row in df.iterrows():
            HistoricalPrices.objects.create(
                date = str(index).split()[0],
                stock_info = stock_info,
                high = row['High'],
                low = row['Low'],
                open = row['Open'],
                close = row['Close'],
                volume = row['Volume']
            )
        self.stdout.write(self.style.SUCCESS(f'***** Finish processing {stock_info.ticker}.TW *****'))

    def add_arguments(self, parser):
        parser.add_argument('-t', '--today', action='store_true', help='Create data only for today')
        parser.add_argument('-s', '--stock', type=str, help='Create data of ONLY the stock\n(Will create data for all stocks if this argument is not used)', )

    def handle(self, *args, **options):
        target = options['stock']
        today = options['today']

        df = pd.DataFrame()

        # with target, do only once
        if target:
            # check if the ticker is valid
            query_set = StockInfo.objects.filter(ticker=target)
            if not query_set.exists():
                self.stdout.write(self.style.DANGER(f'***** {target} doesn\'t exists in our database *****'))
                exit(0)
            ticker = yf.Ticker(f'{target}.TW')
            # period = '1d'
            if today:
                df = ticker.history(period='1d')
            # period = 'max'
            else:
                df = ticker.history(period='max')
            # trim dataframe
            new_df = df.drop(columns=['Dividends', 'Stock Splits'])
            self.saveDf(new_df, query_set[0]) # assume that StockInfo is unique in database
        # without target, do for all stocks
        else:
            # get all ticker from database
            for stock_info in StockInfo.objects.all():
                #####################
                ticker = yf.Ticker(f'{stock_info.ticker}.TW')
                # period = '1d'
                if today:
                    df = ticker.history(period='1d')
                # period = 'max'
                else:
                    df = ticker.history(period='max')
                # trim dataframe
                new_df = df.drop(columns=['Dividends', 'Stock Splits'])
                self.saveDf(new_df, stock_info)
