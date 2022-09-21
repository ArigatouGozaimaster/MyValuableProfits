import yfinance as yf
import sqlite3
import re
from datetime import date
from pandas_datareader import data

from app import price_fetch

"""
Testing
-------
- Fetching Current Real-Time Exchange Rate (USD/AUD) 
- Importing Stock Data Based on Ticker Symbol
- Fetching an Exchange Rate from the past 1300 days (LIMIT)
- Clean up User_id
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

print(price_fetch("qan.ax"))
"""

# Fetching an Exchange Rate from the past 1300 days (LIMIT)
"""
def historic_exchange_rate(purchase_date):
    df = data.DataReader('DEXUSAL', 'fred')
    try:
        value = df.loc[purchase_date, 'DEXUSAL']
    except KeyError:
        value = current_rate() 
    return value

print(historic_exchange_rate('2022-09-15'))
"""


# Update database.db
"""
con = sqlite3.connect("database.db")
cur = con.cursor()

CREATE TABLE portfolio(
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    ticker TEXT NOT NULL,
    name TEXT NOT NULL,
    market TEXT NOT NULL,
    avgprice NUMERIC NOT NULL,
    quantity NUMERIC NOT NULL,
    brokerage NUMERIC NOT NULL,
    buysell TEXT NOT NULL
    );
DROP TABLE portfolio;
"""

# Clean up User_id
"""
def user_id(input):
    id = re.findall("\d+", input)
    var = ''
    for element in id:
        var += str(element)
    user = int(var)
    return user

tag = ("<User 1>")
print(user_id(tag))
"""

# Call get stock price function for Jinja2
"""
@app.context_processor
def stockprice():

    # Get a stock price Jinja2 Function:
    def get_price(ticker):
        stockprice = yf.Ticker(str(ticker).upper())
        print(stockprice.info['regularMarketPrice'])
        if stockprice.info['regularMarketPrice'] is None:
            return ValueError
        elif ".ax" in stockprice:
            return round(stockprice.info['regularMarketPrice'], 2)
        else:
            return round(stockprice.info['regularMarketPrice'] / current_rate(), 2)
    
    return dict(get_price = get_price)
"""