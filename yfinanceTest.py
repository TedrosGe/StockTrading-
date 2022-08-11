import yfinance as yf
msft = yf.Ticker("MSFT")
data = yf.download(tickers = 'PG' )
print(msft.info)