from reports.daily_report import generate_daily_image
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

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

# -----------------------------
# SCHEDULER
# -----------------------------
if __name__ == "__main__":
    scheduler = BlockingScheduler()

    # Escaneo cada 15 minutos
    scheduler.add_job(run_scan, "interval", minutes=15)

    # Resumen cada 1 hora
    scheduler.add_job(hourly_summary, "interval", hours=1)

    # Reporte diario a las 6 PM
    scheduler.add_job(daily_image_report, "cron", hour=18)


    print("⏳ Scanner automático iniciado...")
    scheduler.start()


