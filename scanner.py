from data.market_universe import get_sp500_tickers
import pandas as pd
from datetime import datetime
import time

from reports.daily_report import generate_daily_image
from apscheduler.schedulers.blocking import BlockingScheduler

from data.market_data import get_stock_data
from strategy.indicators import add_indicators
from strategy.signals import generate_signal
from notifications.telegram import send_telegram, send_telegram_image

# -----------------------------
# CONFIGURACIÓN
# -----------------------------
TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN"]
PERIOD = "6mo"

last_signals = {}

# -----------------------------
# ESCANEO PRINCIPAL
# -----------------------------
def run_scan():
    print(f"[{datetime.now()}] Escaneo iniciado")

    for ticker in TICKERS:
        try:
            df = get_stock_data(ticker, period=PERIOD)
            df = add_indicators(df)
            signal = generate_signal(df)

            previous_signal = last_signals.get(ticker)

            if signal != previous_signal:
                message = (
                    f"📊 Cambio de señal detectado\n"
                    f"Acción: {ticker}\n"
                    f"Nueva señal: {signal}"
                )
                send_telegram(message)
                last_signals[ticker] = signal

        except Exception as e:
            print(f"Error escaneando {ticker}: {e}")

OUTPUT_FILE = "daily_market_scan.csv"

def run_daily_scan():
    tickers = get_sp500_tickers()
    results = []

    buy_list = []
    sell_list = []

    for i, ticker in enumerate(tickers):
        try:
            df = get_stock_data(ticker, period="6mo")

            if df is None or len(df) < 60:
                continue

            df = add_indicators(df)
            signal = generate_signal(df)

            price = round(df.iloc[-1]["Close"], 2)
            rsi = round(df.iloc[-1]["RSI"], 2)

            results.append({
                "ticker": ticker,
                "signal": signal,
                "price": price,
                "rsi": rsi
            })

            if signal == "BUY":
                buy_list.append(f"{ticker} (${price}, RSI {rsi})")

            elif signal == "SELL":
                sell_list.append(f"{ticker} (${price}, RSI {rsi})")

            # evitar bloqueos de Yahoo
            if i % 25 == 0:
                time.sleep(1)

        except Exception:
            continue

    # Guardar resultados para Streamlit
    pd.DataFrame(results).to_csv(OUTPUT_FILE, index=False)

    send_daily_summary(buy_list, sell_list)

def daily_image_report():
    for ticker in TICKERS:
        try:
            image = generate_daily_image(ticker)
            send_telegram_image(
                image,
                caption=f"📈 Reporte diario {ticker}"
            )
        except Exception as e:
            print(f"Error reporte diario {ticker}: {e}")

# -----------------------------
# RESUMEN HORARIO
# -----------------------------
def hourly_summary():
    if not last_signals:
        return

    message = "🕐 Resumen horario\n\n"
    for ticker, signal in last_signals.items():
        message += f"{ticker}: {signal}\n"

    send_telegram(message)

def send_daily_summary(buy_list, sell_list):
    today = datetime.now().strftime("%Y-%m-%d")

    message = f"<b>📊 Resumen Diario del Mercado</b>\n📅 {today}\n\n"

    message += "<b>🟢 Oportunidades de COMPRA</b>\n"
    message += "\n".join(buy_list[:15]) if buy_list else "Sin señales BUY hoy"
    message += "\n\n"

    message += "<b>🔴 Señales de VENTA</b>\n"
    message += "\n".join(sell_list[:15]) if sell_list else "Sin señales SELL hoy"

    send_telegram(message)

# -----------------------------
# SCHEDULER
# -----------------------------
if __name__ == "__main__":
    scheduler = BlockingScheduler()

    # Escaneo cada 5 minutos
    scheduler.add_job(run_scan, "interval", minutes=5)

    # Resumen cada 1 hora
    scheduler.add_job(hourly_summary, "interval", hours=1)

    # Reporte diario a las 6 PM
    scheduler.add_job(daily_image_report, "cron", hour=18)

    run_daily_scan()

    print("⏳ Scanner automático iniciado...")
    scheduler.start()


