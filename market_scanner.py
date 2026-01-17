import pandas as pd
from data.market_data import get_stock_data
from strategy.indicators import rsi, moving_average
from strategy.signals import generate_signal
from notifications.telegram import send_telegram
from data.market_universe import get_sp500_tickers

PERIOD = "6mo"
results = []

tickers = get_sp500_tickers()

for ticker in tickers:
    try:
        df = get_stock_data(ticker, period=PERIOD)

        df["MA_20"] = moving_average(df["Close"], 20)
        df["MA_50"] = moving_average(df["Close"], 50)
        df["RSI"] = rsi(df["Close"])

        signal = generate_signal(df)

        results.append({
            "ticker": ticker,
            "price": round(df.iloc[-1]["Close"], 2),
            "rsi": round(df.iloc[-1]["RSI"], 2),
            "signal": signal
        })

    except Exception:
        continue

df_results = pd.DataFrame(results)
df_results.to_csv("daily_market_scan.csv", index=False)

buy = df_results[df_results["signal"] == "BUY"]
sell = df_results[df_results["signal"] == "SELL"]

buy_list = buy["ticker"].astype(str).tolist()[:10]
sell_list = sell["ticker"].astype(str).tolist()[:10]

message = "<b>📊 Escaneo Diario S&P 500</b>\n\n"

message += f"🟢 BUY ({len(buy)}): "
message += ", ".join(buy_list) if buy_list else "Ninguna"
message += "\n"

message += f"🔴 SELL ({len(sell)}): "
message += ", ".join(sell_list) if sell_list else "Ninguna"
message += "\n\n"

message += "📁 CSV generado con el detalle completo."

send_telegram(message)
