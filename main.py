from data.market_data import get_stock_data
from strategy.indicators import rsi, moving_average
from strategy.signals import generate_signal
from notifications.email import send_email
from notifications.telegram import send_telegram
from state import load_state, save_state

TICKERS = ["AAPL", "MSFT", "GOOGL", "TTWO", "AMZN"]


def run_assistant():

    state = load_state()

    for ticker in TICKERS:
        df = get_stock_data(ticker)

        df["RSI"] = rsi(df["Close"])
        df["MA_20"] = moving_average(df["Close"], 20)
        df["MA_50"] = moving_average(df["Close"], 50)

        signal = generate_signal(df)
        last_signal = state.get(ticker)

        if signal != "HOLD" and signal != last_signal:
            message = (
                f"📊 Alerta de Inversión\n\n"
                f"Activo: {ticker}\n"
                f"Señal: {signal}\n"
                f"Precio: {round(df.iloc[-1]['Close'], 2)}\n"
                f"RSI: {round(df.iloc[-1]['RSI'], 2)}"
            )

            send_email(
                subject=f"Alerta {signal} - {ticker}",
                body=message
            )

            send_telegram(message)

            state[ticker] = signal

    save_state(state)

if __name__ == "__main__":
    run_assistant()
