import pandas_ta as ta

def apply_indicators(df):
    df["RSI"] = ta.rsi(df["Close"])
    return df
