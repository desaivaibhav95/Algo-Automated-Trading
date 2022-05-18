import yfinance as yf
import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import time
import os
import smtplib
import imghdr
from email.message import EmailMessage

email_address = 'vaibhavdesai866@gmail.com'
email_password = 'nrwnrbkqlvfufxhb'

message=EmailMessage()

yf.pdr_override()
start=dt.datetime(2022,1,1)
now=dt.datetime.now()

stock="LT.NS"
TargetPrice=1800

message['Subject']="Price Alert on "+str(stock)+"!"
message['From']=email_address
message['To']="hbs2595@gmail.com"

alerted=False

while 1:
    df=pdr.get_data_yahoo(stock,start,now)
    current_close=df['Adj Close'][-1]

    condition = current_close>TargetPrice

    if (condition and alerted == False):
        alerted=True
        msg=str(stock)+" has crossed the target price of "+str(TargetPrice)+\
        "\n Current Price : "+str(current_close)
        print(msg)
        message.set_content(msg)

        with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
            smtp.login(email_address,email_password)
            smtp.send_message(message)

            print("Completed")
    else:
        print("No New Alerts")
    time.sleep(300)
