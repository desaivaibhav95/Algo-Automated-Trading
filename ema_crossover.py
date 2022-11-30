import pandas as pd
import numpy as np
import yfinance as yf
import talib
import datetime as dt
from pandas_datareader import data as pdr

yf.pdr_override()
import pandas_ta as ta

import seaborn as sns

#import chart_studio.plotly as py
#import plotly.offline as plyo
#plyo.init_notebook_mode(connected=True)

#import plotly.express as px
#import plotly.graph_objects as go
#from plotly.subplots import make_subplots

ticker = input("Enter Stock Ticker : ")
print(ticker)

startyear=2012
startmonth=1
startday=1

start=dt.datetime(startyear,startmonth,startday)

end=dt.datetime.now()

df=pdr.get_data_yahoo(ticker,start,end)


data = pd.DataFrame({'Close' : df['Close'],
                     'EMA (10 days)' : talib.EMA(df['Close'], timeperiod = 10),
                     'EMA (20 days)' : talib.EMA(df['Close'], timeperiod = 20),
                     'EMA (30 days)' : talib.EMA(df['Close'], timeperiod = 30)})

data = data.reset_index().dropna(axis=0)

#fig = make_subplots(rows=2,cols=1)
#fig.add_trace(go.Scatter(x=data.iloc[-200:]['Date'],y=data.iloc[-200:]['Close'],name="Close Price",marker={'color': 'blue'}),row=1,col=1)
#fig.add_trace(go.Scatter(x=data.iloc[-200:]['Date'],y=data.iloc[-200:]['EMA (10 days)'],name="EMA (10 days)",marker={'color': 'red'}),row=2,col=1)
#fig.add_trace(go.Scatter(x=data.iloc[-200:]['Date'],y=data.iloc[-200:]['EMA (20 days)'],name="EMA (20 days)",marker = {'color' : 'green'}),row=2,col=1)
#fig.add_trace(go.Scatter(x=data.iloc[-200:]['Date'],y=data.iloc[-200:]['EMA (30 days)'],name="EMA (30 days)",marker = {'color' : 'purple'}),row=2,col=1)

#fig.update_yaxes(title_text="Close Price", row=1, col=1)
#fig.update_yaxes(title_text="EMA (10 vs 20 vs 30 days)", row=2, col=1)

#fig.update_layout(title='Close Price vs EMA (10 vs 20 vs 30 days)',height=900, width=1000,template = 'plotly_dark')

buy_calls = []
sell_calls = []

buy_prices = []
sell_prices = []

buy_dates = []
sell_dates = []

positions_list = []

pos = 0

for i in data.index:
    if (data['EMA (10 days)'][i] > data['EMA (20 days)'][i] > data['EMA (30 days)'][i]):  # --(a)
        if (pos == 0):                                                                    # --(b)
            bp = data['Close'][i]                                                         # --(c)
            pos = 1                                                                       # --(d)

            #print('Buy Call at '+str(bp)+' on '+ str(data['Date'][i]))                    # --(e)

            call_type = "buy"                                                             # --(f)
            buy_date = data['Date'][i]                                                    # --(g)

            positions_list.append(pos)                                                    # --(h)

            buy_calls.append(call_type)                                                   # --(i)
            buy_prices.append(bp)                                                         # --(j)
            buy_dates.append(buy_date)                                                    # --(k)

    if (data['EMA (10 days)'][i] < data['EMA (20 days)'][i] < data['EMA (30 days)'][i])\
      |(data['EMA (10 days)'][i] < data['EMA (30 days)'][i] < data['EMA (20 days)'][i]):
        if (pos == 1):
            sp = data['Close'][i]
            pos = 0

            #print('Sell Call at '+str(sp)+' on '+ str(data['Date'][i]))

            call_type = "sell"
            sell_date = data['Date'][i]

            positions_list.append(pos)

            sell_calls.append(call_type)
            sell_prices.append(sp)
            sell_dates.append(sell_date)

buy_all = pd.DataFrame({'Calls':buy_calls,
                        'Date':buy_dates,
                        'Price':buy_prices,
                        })

sell_all = pd.DataFrame({'Calls':sell_calls,
                        'Date':sell_dates,
                        'Price':sell_prices,
                        })

buy_all['Price'] = buy_all['Price']*1.01 # 1% for Buy Orders
sell_all['Price'] = sell_all['Price']*0.98 # 2% for Sell Orders

all_calls = pd.concat(objs=[buy_all,sell_all],axis=0).sort_values('Date')

all_calls['P&L(Amount)'] = all_calls.groupby(all_calls.Calls.eq('buy').cumsum())['Price'].diff()
all_calls['P&L(%)'] = (all_calls.groupby(all_calls.Calls.eq('buy').cumsum())['Price'].pct_change())*100
all_calls['Time in Trade'] = all_calls.groupby(all_calls.Calls.eq('buy').cumsum())['Date'].diff()

P_n_L = pd.DataFrame({'Strategy Success Rate (%)':round(all_calls.loc[all_calls['P&L(%)']>=0]['P&L(%)'].count()\
                                                        /(all_calls['P&L(%)'].count())*100,2),
                         'Avg. Gain of Profitable Trades (%)':round(all_calls.loc[all_calls['P&L(%)']>=0]['P&L(%)']\
                                                                    .mean(),2),
                         'Max. Gain of Profitable Trades (%)':round(all_calls.loc[all_calls['P&L(%)']>=0]['P&L(%)']\
                                                                    .max(),2),
                         'Avg. Loss of all loss making Trades (%)':round(all_calls.loc[all_calls['P&L(%)']<0]['P&L(%)']\
                                                                         .mean(),2),
                         'Max. Loss of all loss making Trades (%)':round(all_calls.loc[all_calls['P&L(%)']<0]['P&L(%)']\
                                                                         .min(),2),
                         'Number of Trades Taken':round((all_calls['Calls'].count()/2),0),
                         'Avg. Time in a Trade (days)':round(all_calls['Time in Trade'].dt.days.mean(),0)
                         },index=[0])

P_n_L.style.format({'Strategy Success Rate (%)':'{:.1f}%',
                          'Avg. Gain of Profitable Trades (%)':'{:.1f}%',
                          'Max. Gain of Profitable Trades (%)':'{:.1f}%',
                          'Avg. Loss of all loss making Trades (%)':'{:.1f}%',
                          'Max. Loss of all loss making Trades (%)':'{:.1f}%',
                          'Number of Trades Taken':'{:.0f}',
                          'Avg. Time in a Trade (days)':'{:.0f} days'})\
           .bar(subset = ['Strategy Success Rate (%)',
                          'Avg. Gain of Profitable Trades (%)',
                          'Max. Gain of Profitable Trades (%)',
                          'Avg. Loss of all loss making Trades (%)',
                          'Max. Loss of all loss making Trades (%)'],
               color = ['red','green'],align='zero')\
           .bar(subset = ['Number of Trades Taken','Avg. Time in a Trade (days)'],color=['blue'],align='mid')
