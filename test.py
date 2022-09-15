import yfinance as yf


# ticker = yf.Ticker(input_ticker)
ticker = yf.Ticker("QAN.AX")
print(ticker.info['regularMarketPrice'])
ticker = yf.Ticker("BOGUSTICK")
print(ticker.info['regularMarketPrice'])