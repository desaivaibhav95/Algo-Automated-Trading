import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os
from pandas import ExcelWriter

stock_screener = pd.read_excel(r"C:\Users\Hp\Downloads\5_6303176652218171831.xlsx")

nse_stocks = stock_screener[stock_screener['NSE Code'].notnull()]
nse_stock_list = nse_stocks
screened_list = pd.DataFrame(columns=['Stock','P/E','Sales growth(3 years)','Margin growth(3 years)','P/B ratio','Debt-to-equity ratio','EVEBITDA'])
for i in nse_stock_list.index:
    stock = str(nse_stock_list['NSE Code'][i])
    P_E = float(nse_stock_list['Price to Earning'][i])
    Sales_growth_3years = float(nse_stock_list['Sales growth 3Years'][i])
    Margin_growth_3years = float(nse_stock_list['Profit growth 3Years'][i])
    P_B = float(nse_stock_list['Price to book value'][i])
    debt_to_equity = float(nse_stock_list['Debt to equity'][i])
    ev_ebitda = float(nse_stock_list['EVEBITDA'][i])

    if (P_E<20):
        cond_1=True
    else:
        cond_1=False

    if (Sales_growth_3years>10):
        cond_2=True
    else:
        cond_2=False

    if (Margin_growth_3years>10):
        cond_3=True
    else:
        cond_3=False

    if (P_B<4):
        cond_4=True
    else:
        cond_4=False

    if (P_E<20):
        cond_5=True
    else:
        cond_5=False

    if (debt_to_equity<1):
        cond_6=True
    else:
        cond_6=False


    if(cond_1 and cond_2 and cond_3 and cond_4 and cond_5 and cond_6):
         screened_list = screened_list.append({'Stock': stock, 'P/E': P_E, 'Sales growth(3 years)': Sales_growth_3years, 'Margin growth(3 years)': Margin_growth_3years, 'P/B ratio': P_B,'Debt-to-equity ratio': debt_to_equity, 'EVEBITDA': ev_ebitda}, ignore_index=True)

print(screened_list)
