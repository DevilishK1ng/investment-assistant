import matplotlib.pyplot as plt
from datetime import date
import os

from data.market_data import get_stock_data
from strategy.indicators import add_indicators

def generate_daily_image(ticker):
    df = get_stock_data(ticker, "1y")
    df = add_indicators(df)

    plt.figure(figsize=(10, 5))
    plt.plot(df["Close"], label="Precio")
    plt.plot(df["MA_20"], label="MA 20")
    plt.plot(df["MA_50"], label="MA 50")
    plt.title(f"{ticker} - Reporte diario")
    plt.legend()

    filename = f"reports/{ticker}_{date.today()}.png"
    plt.savefig(filename)
    plt.close()

    return filename
