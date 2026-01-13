from data.company_info import get_company_info
from data.market_data import get_stock_data
from strategy.indicators import rsi, moving_average
from strategy.signals import generate_signal

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import os

# -------------------------------------------------
# CONFIGURACIÓN GENERAL
# -------------------------------------------------
st.set_page_config(page_title="Investment Assistant", layout="wide")
st.title("📊 Investment Assistant Dashboard")

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
st.sidebar.header("Configuración")

view_mode = st.sidebar.radio(
    "Modo de visualización",
    ["Análisis por Acción", "Escaneo Diario del Mercado"]
)

# -------------------------------------------------
# MODO 1: ANÁLISIS POR ACCIÓN (TU LÓGICA ACTUAL)
# -------------------------------------------------
if view_mode == "Análisis por Acción":

    tickers_input = st.sidebar.text_input(
        "Acciones a monitorear (separadas por coma)",
        value="AAPL,MSFT,GOOGL,TTWO"
    )

    period = st.sidebar.selectbox(
        "Periodo de análisis",
        ["3mo", "6mo", "1y", "2y"],
        index=1
    )

    tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

    for ticker in tickers:
        st.subheader(f"📈 {ticker}")

        try:
            # -------- INFO EMPRESA --------
            info = get_company_info(ticker)

            col_info1, col_info2, col_info3 = st.columns(3)

            col_info1.markdown(f"**Empresa:** {info['name']}")
            col_info1.markdown(f"**Sector:** {info['sector']}")
            col_info1.markdown(f"**Industria:** {info['industry']}")

            if info.get("market_cap"):
                market_cap_billions = info["market_cap"] / 1_000_000_000
                col_info2.metric("Capitalización", f"${market_cap_billions:.2f} B")

            if info.get("pe_ratio"):
                col_info3.metric("P/E", round(info["pe_ratio"], 2))

            # -------- DATOS DE MERCADO --------
            df = get_stock_data(ticker, period=period)

            df["MA_20"] = moving_average(df["Close"], 20)
            df["MA_50"] = moving_average(df["Close"], 50)
            df["RSI"] = rsi(df["Close"])

            signal = generate_signal(df)

            col1, col2, col3 = st.columns(3)
            col1.metric("Precio actual", f"${round(df.iloc[-1]['Close'], 2)}")
            col2.metric("RSI", round(df.iloc[-1]['RSI'], 2))
            col3.metric("Señal", signal)

            # -------- GRÁFICO PRECIO --------
            fig1, ax1 = plt.subplots()
            ax1.plot(df["Close"], label="Precio", linewidth=2)
            ax1.plot(df["MA_20"], label="MA 20 (Corto plazo)", linestyle="--")
            ax1.plot(df["MA_50"], label="MA 50 (Mediano plazo)", linestyle=":")
            ax1.set_title("Precio y Medias Móviles")
            ax1.legend()
            st.pyplot(fig1)

            st.caption(
                "MA 20: tendencia de corto plazo (~1 mes). "
                "MA 50: tendencia de mediano plazo (~2–3 meses). "
                "Cruces entre ambas pueden indicar cambios de tendencia."
            )

            # -------- GRÁFICO RSI --------
            fig2, ax2 = plt.subplots()
            ax2.plot(df["RSI"], label="RSI")
            ax2.axhline(30, linestyle="--")
            ax2.axhline(70, linestyle="--")
            ax2.set_title("RSI")
            ax2.legend()
            st.pyplot(fig2)

            st.divider()

        except Exception as e:
            st.error(f"Error cargando {ticker}: {e}")

# -------------------------------------------------
# MODO 2: ESCANEO DIARIO DEL MERCADO (CSV)
# -------------------------------------------------
else:
    st.header("🌍 Escaneo Diario del Mercado")

    csv_file = "daily_market_scan.csv"

    if not os.path.exists(csv_file):
        st.warning(
            "⚠️ Aún no se ha generado el escaneo diario.\n\n"
            "Ejecuta el scanner diario para ver resultados."
        )
    else:
        df = pd.read_csv(csv_file)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("🟢 BUY")
            st.dataframe(
                df[df["signal"] == "BUY"]
                .sort_values("rsi")
                .reset_index(drop=True),
                use_container_width=True
            )

        with col2:
            st.subheader("🟡 HOLD")
            st.dataframe(
                df[df["signal"] == "HOLD"]
                .reset_index(drop=True),
                use_container_width=True
            )

        with col3:
            st.subheader("🔴 SELL")
            st.dataframe(
                df[df["signal"] == "SELL"]
                .sort_value_("rsi", ascending=False)
                .reset_index(drop=True),
                use_container_width=True
            )

        st.caption(
            "Este escaneo se genera automáticamente al cierre del mercado "
            "y utiliza la misma estrategia MA20 / MA50 / RSI."
        )
