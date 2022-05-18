import pandas as pd
import numpy as np
import yfinance as yf
from pandas_datareader import data as pdr
import datetime as dt
from pandas import ExcelWriter
import talib
pd.set_option('display.max_rows', None)
yf.pdr_override()

start = dt.datetime(2022,1,1)
now=dt.datetime.now()

nse_stocks = pd.read_csv(r'C:\Users\Hp\Documents\EQUITY_L.csv')
nse_stocks['SYMBOL']=nse_stocks['SYMBOL']+".NS"
nse_stocks_sample = nse_stocks.iloc[:100]


screened_list = pd.DataFrame(columns=['Stock','Last Close','EMA_20','EMA_50','RSI','MACD'])

for i in nse_stocks.index:
    stock = str(nse_stocks['SYMBOL'][i])

    try:
        df=pdr.get_data_yahoo(stock,start,now)

        emas = [20,50]
        for x in emas:
            ema=x
            df["EMA_"+str(ema)]=round(df.iloc[:,4].rolling(window=ema).mean(),2)

        RSI=talib.RSI(df["Adj Close"],timeperiod=14)[-1]
        MACD=talib.MACDFIX(df['Close'],signalperiod=9)[0][-1]
        last_close=df["Adj Close"][-1]
        ema_20=df["EMA_20"][-1]
        ema_50=df["EMA_50"][-1]

        if (last_close>ema_20):
            condition_1=True
        else:
            condition_1=False

        if (last_close>ema_50):
            condition_2=True
        else:
            condition_2=False

        if (65>=RSI>=55):
            condition_3=True
        else:
            condition_3=False

        if (2>=MACD>=-2):
            condition_4=True
        else:
            condition_4=False

        if (condition_1 and condition_2 and condition_3 and condition_4):
            screened_list = screened_list.append({'Stock':stock,'Last Close':last_close,'EMA_20':ema_20,'EMA_50':ema_50,'RSI':RSI,'MACD':MACD},ignore_index=True)
    except:
        print("No Stock Data Available")

print(screened_list)
