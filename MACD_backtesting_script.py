import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import talib
import datetime as dt
from pandas_datareader import data as pdr

yf.pdr_override()

# Use .BO for BSE stock data
ticker = input("Enter Stock Ticker : ")
print(ticker)

startyear=2012
startmonth=1
startday=1

start=dt.datetime(startyear,startmonth,startday)

now=dt.datetime.now()

df=pdr.get_data_yahoo(ticker,start,now)

df = pd.DataFrame({#'Date':df.index,
                    'Close':df['Close'],
                    'Price SMA (21 days)':talib.SMA(df['Close'], timeperiod=21),
                    'Price SMA (50 days)':talib.SMA(df['Close'], timeperiod=50),
                    'Volume SMA (16 days)':talib.SMA(df['Volume'], timeperiod=16),
                    'MACD':talib.MACD(df['Close'], signalperiod=9)[0],
                    'Signal':talib.MACD(df['Close'], signalperiod=9)[1]})

df = df.iloc[49:]

df['MACD'] = round(df['MACD'],ndigits=2)
df['Signal'] = round(df['Signal'],ndigits=2)

df.reset_index(inplace=True)

# P&L buy first

calls= []
pos=0
num=0
per_chg = []

for i in df.index:
    if (df['MACD'][i]>df['Signal'][i])&(df['MACD'].shift(-1)[i]<df['Signal'].shift(-1)[i]):
        if(pos==0):
            bp=df['Close'][i]
            pos=1
            print("Buy Call at "+str(bp)+" on "+str(df['Date'][i]))
    elif (df['MACD'][i]<df['Signal'][i])&(df['MACD'].shift(-1)[i]>df['Signal'].shift(-1)[i]):
        if(pos==1):
            sp = df['Close'][i]
            pos=0
            print("Sell call at "+str(sp)+" on "+str(df['Date'][i]))
            pc = (sp/bp-1)*100
            per_chg.append(pc)
    else:
        pass
    num+=1


gains=0
ng=0
losses=0
nl=0
total_ret = 1

for i in per_chg:
    if(i>0):
        gains+=i
        ng+=1
    else:
        losses+=i
        nl+=1
    total_ret=total_ret*((i/100)+1)

total_ret = round((total_ret-1)*100,2)

if (ng>0):
    avgGain=gains/ng
    maxR=str(round(max(per_chg),2))
else:
    avgGain=0
    maxR="undefined"

if (nl>0):
    avgLoss=losses/nl
    maxL=str(round(min(per_chg),2))
    ratio=str(round(-avgGain/avgLoss,2))
else:
    avgLoss=str(min(per_chg))
    RATIO="inf"
if (ng>0 or nl>0):
    battingAvg=ng/(ng+nl)
else:
    battingAvg=0

print()
print("Results for "+ ticker +" going back to "+str(startyear)+", Sample size: "+str(ng+nl)+" trades")
#print("Batting Avg: "+ str(battingAvg))
print("Strategy Success Rate: "+ str(round(battingAvg*100,2))+"%")
print("Gain/loss ratio: "+ ratio)
print("Average Gain: "+ str(round(avgGain,2))+"%")
print("Average Loss: "+ str(round(avgLoss,2))+"%")
print("Max Return: "+ maxR+"%")
print("Max Loss: "+ maxL+"%")
print("Total return over "+str(ng+nl)+ " trades: "+ str(total_ret)+"%" )
#print("Example return Simulating "+str(n)+ " trades: "+ str(nReturn)+"%" )
#print()
