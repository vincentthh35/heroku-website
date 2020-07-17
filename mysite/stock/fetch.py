import talib
import requests
import os
import pandas as pd
import pickle
import yfinance as yf
from .models import HistoricalPrices
from django.conf import settings
from sqlalchemy import create_engine

# absolute path
ABS_PATH = os.path.abspath(os.path.dirname(__file__))

# user = settings.DATABASES['default']['USER']
# password = settings.DATABASES['default']['PASSWORD']
# database_name = settings.DATABASES['default']['NAME']
#
# database_url = 'postgresql://{user}:{password}@localhost:5432/{database_name}'.format(
#     user=user,
#     password=password,
#     database_name=database_name,
# )

def dump_df(target, pathname):
    f = open(pathname, 'wb')
    pickle.dump(target, f)
    f.close()

def fetch_df():
    res = requests.get("http://isin.twse.com.tw/isin/C_public.jsp?strMode=2")
    df = pd.read_html(res.text)[0]
    df.columns = df.iloc[0]
    df = df.iloc[1:]
    df = df.drop(1)
    df = df.dropna(thresh=3, axis=0).dropna(thresh=3, axis=1)
    # len(id) == 4
    df = df[ df['有價證券代號及名稱'].str.split().str[0].str.len() == 4 ]

    df = df.reset_index(drop=True)

    new_df = df['有價證券代號及名稱'].str.replace(u'\u3000',' ').str.split(u' ',expand=True)
    new_df.columns = ['Ticker', 'StockName']
    new_df['Sector'] = df['產業別']
    print(new_df)
    return new_df

def fetch():
    if os.path.isfile(f'{ABS_PATH}/data/stock_name_list'):
        f = open(f'{ABS_PATH}/data/stock_name_list', 'rb')
        df = pickle.load(f)
        f.close()
    else:
        df = fetch_df()
        dump_df(df, f'{ABS_PATH}/data/stock_name_list')

    stock_df = pd.DataFrame()

    ticker_list = df['Ticker'].head(3)
    for ticker in ticker_list:
        print(f'*** Downloading {ticker} ***')
        stock = yf.Ticker(f'{ticker}.TW')
        temp_df = stock.history()
        # TODO : Date column
        temp_df['date'] = temp_df.index
        temp_df['ticker'] = ticker
        temp_df['open'] = temp_df['Open']
        temp_df['high'] = temp_df['High']
        temp_df['low'] = temp_df['Low']
        temp_df['close'] = temp_df['Close']
        temp_df['volume'] = temp_df['Volume']
        stock_df = pd.concat([ stock_df, temp_df ], axis=0)

    stock_df = stock_df.reset_index(drop=True)
    stock_df = stock_df[['date','ticker','open','high','low','close','volume']]
    stock_df = stock_df.astype(str)
    # engine = create_engine(database_url, echo=False)
    engine = create_engine('sqlite:///db.sqlite3')
    stock_df.to_sql(HistoricalPrices, con=engine)
    return stock_df
    # print(stock_df)
