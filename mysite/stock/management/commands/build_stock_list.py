import requests
import pandas as pd
from django.core.management.base import BaseCommand
from stock.models import StockInfo

class Command(BaseCommand):
    help = 'build the list of stock information'

    def handle(self, *args, **options):
        try:
            res = requests.get("http://isin.twse.com.tw/isin/C_public.jsp?strMode=2")
        except:
            self.stdout.write(self.style.ERROR('could not get information from twse website!'))
        df = pd.read_html(res.text)[0]
        df.columns = df.iloc[0]
        df = df.iloc[1:]
        df = df.drop(1)
        df = df.dropna(thresh=3, axis=0).dropna(thresh=3, axis=1)
        df = df[ df['有價證券代號及名稱'].str.split().str[0].str.len() == 4 ]
        df = df.reset_index(drop=True)
        new_df = df['有價證券代號及名稱'].str.replace(u'\u3000',' ').str.split(u' ',expand=True)
        new_df.columns = ['Ticker', 'StockName']
        new_df['Sector'] = df['產業別']

        # parse through rows
        for index, row in new_df.iterrows():
            ticker = row['Ticker']
            stock_name = row['StockName']
            sector = row['Sector']
            if pd.isna(sector):
                sector = '無'

            self.stdout.write(f'***** begin processing {ticker} {stock_name} *****')
            # if old record exists
            if StockInfo.objects.filter(ticker=ticker, stock_name=stock_name, sector=sector).exists():
                self.stdout.write(self.style.NOTICE(f'***** data \'{ticker} {stock_name}\' already exists! *****'))
            else:
                try:
                    StockInfo.objects.create(
                        ticker=ticker,
                        stock_name=stock_name,
                        sector=sector
                    )
                    self.stdout.write(self.style.SUCCESS(f'***** data \'{ticker} {stock_name}\' has been successfully written! *****'))
                except:
                    self.stderr.write(self.style.ERROR(f'***** Something wrong happened while writing data \'{ticker} {stock_name}\' *****'))
