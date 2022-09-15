import yfinance as yf
from datetime import date
from pandas_datareader import data

"""
Testing
-------
- Fetching Current Real-Time Exchange Rate (USD/AUD) 
- Importing Stock Data Based on Ticker Symbol
- Fetching an Exchange Rate from the past 1300 days (LIMIT)
"""


# Fetching Current Real-Time Exchange Rate (USD/AUD) 
"""
AUD = data.DataReader('DEXUSAL', 'fred')
a = AUD.DEXUSAL.iat[-1]

"""

# Importing Stock Data based on Ticker
"""
stock = "aapl"
ticker = yf.Ticker(str(stock).upper())
if ticker.info['regularMarketPrice'] is None:
    print("Undefined")
elif ".ax" in stock:
    print(round(ticker.info['regularMarketPrice'], 2))
else:
    print(round(ticker.info['regularMarketPrice'] / a, 2))
"""

# Fetching an Exchange Rate from the past 1300 days (LIMIT)
""""""
today = date.today()
print(today)

AUD = data.DataReader('DEXUSAL', 'fred')