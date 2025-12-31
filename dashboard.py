import matplotlib.pyplot as plt
from data.market_data import get_stock_data
from strategy.indicators import rsi, moving_average

ticker = "AAPL"

df = get_stock_data(ticker)

df["MA_20"] = moving_average(df["Close"], 20)
df["MA_50"] = moving_average(df["Close"], 50)
df["RSI"] = rsi(df["Close"])

plt.figure()
plt.plot(df["Close"], label="Precio")
plt.plot(df["MA_20"], label="MA 20")
plt.plot(df["MA_50"], label="MA 50")
plt.legend()
plt.title(f"{ticker} - Precio y Medias")
plt.show()

plt.figure()
plt.plot(df["RSI"], label="RSI")
plt.axhline(30)
plt.axhline(70)
plt.title("RSI")
plt.legend()
plt.show()
