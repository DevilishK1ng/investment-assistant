from data.market_data import get_stock_data
from strategy.indicators import rsi, moving_average
from strategy.signals import generate_signal

df = get_stock_data("AAPL")

df["RSI"] = rsi(df["Close"])
df["MA_20"] = moving_average(df["Close"], 20)
df["MA_50"] = moving_average(df["Close"], 50)

signal = generate_signal(df)

print("Señal actual:", signal)