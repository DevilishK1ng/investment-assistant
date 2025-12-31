import pandas as pd

def generate_signal(df: pd.DataFrame) -> str:
    """
    Retorna BUY, SELL o HOLD según reglas técnicas.
    """

    if len(df) < 50:
        return "HOLD"

    prev = df.iloc[-2]
    last = df.iloc[-1]

    ma20_prev = prev["MA_20"].item()
    ma50_prev = prev["MA_50"].item()
    ma20_last = last["MA_20"].item()
    ma50_last = last["MA_50"].item()
    rsi_last = last["RSI"].item()

    ma_cross_up = ma20_prev < ma50_prev and ma20_last > ma50_last
    ma_cross_down = ma20_prev > ma50_prev and ma20_last < ma50_last

    if rsi_last < 30 and ma_cross_up:
        return "BUY"

    if rsi_last > 70 and ma_cross_down:
        return "SELL"

    return "HOLD"
