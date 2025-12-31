import yfinance as yf

def get_data(ticker):
    return yf.download(ticker, period="6mo", interval="1d")
