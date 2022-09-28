import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr
yf.pdr_override()

ticker = input("Enter Stock Ticker : ")
print(ticker)

startyear=2012
startmonth=1
startday=1

start=dt.datetime(startyear,startmonth,startday)

end=dt.datetime.now()

stock_ma=pdr.get_data_yahoo(ticker,start,end)

# Simple Moving Average
stock_ma['SMA_5'] = stock_ma['Close'].rolling(5).mean()
stock_ma['SMA_10'] = stock_ma['Close'].rolling(10).mean()

# Exponential Moving Average
stock_ma['EMA_5'] = stock_ma['Close'].ewm(span = 5, min_periods = 4).mean()
stock_ma['EMA_10'] = stock_ma['Close'].ewm(span = 10, min_periods = 9).mean()

print (stock_ma)
