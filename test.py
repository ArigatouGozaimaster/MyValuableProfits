import yfinance as yf
import sqlite3
from datetime import date
from pandas_datareader import data

from app import price_fetch

"""
Testing
-------
- Fetching Current Real-Time Exchange Rate (USD/AUD) 
- Importing Stock Data Based on Ticker Symbol
- Fetching an Exchange Rate from the past 1300 days (LIMIT)
"""


# Fetching Current Real-Time Exchange Rate (USD/AUD) 
"""
def current_rate():
    AUD = data.DataReader('DEXUSAL', 'fred')
    current_exchange_rate = AUD.DEXUSAL.iat[-1]
    return current_exchange_rate
"""

# Importing Stock Data based on Ticker (Dependant on current_rate)
"""
def price_fetch(stock):
    ticker = yf.Ticker(str(stock).upper())
    if ticker.info['regularMarketPrice'] is None:
        return ValueError

    elif ".ax" in stock:
        return round(ticker.info['regularMarketPrice'], 2)

    else:
        return round(ticker.info['regularMarketPrice'] / current_rate(), 2)

print(price_fetch("aapdsal"))
"""

# Fetching an Exchange Rate from the past 1300 days (LIMIT)
"""
def historic_exchange_rate(purchase_date):
    df = data.DataReader('DEXUSAL', 'fred')
    value = df.loc[purchase_date, 'DEXUSAL']
    return value

print(historic_exchange_rate("2020-03-27"))
"""

# Update database.db
"""
con = sqlite3.connect("database.db")
cur = con.cursor()

CREATE TABLE portfolio(
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    ticker TEXT NOT NULL,
    quantity NUMERIC NOT NULL,
    purchaseprice NUMERIC NOT NULL,
    date NUMERIC NOT NULL,
    buysell TEXT NOT NULL
    );
DROP TABLE portfolio;
"""