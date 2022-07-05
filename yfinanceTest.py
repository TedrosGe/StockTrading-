import yfinance as yf
msft = yf.Ticker("PG")
data = yf.download(tickers = 'AMZN', period= '1d', interval= '60m' )
print(data)