import yfinance as yf
import pandas as pd

def get_stock_data(ticker: str, period="6mo", interval="1d") -> pd.DataFrame:
    """
    Descarga datos históricos de una acción.
    """
    data = yf.download(
        tickers=ticker,
        period=period,
        interval=interval,
        progress=False
    )

    return data
