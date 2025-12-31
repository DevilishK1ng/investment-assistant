import pandas as pd

def rsi(data: pd.Series, period: int = 14) -> pd.Series:
    delta = data.diff()

    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def moving_average(data: pd.Series, window: int) -> pd.Series:
    return data.rolling(window=window).mean()

def moving_average(series, window):
    return series.rolling(window=window).mean()

def rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def add_indicators(df):
    df = df.copy()
    df["MA_20"] = moving_average(df["Close"], 20)
    df["MA_50"] = moving_average(df["Close"], 50)
    df["RSI"] = rsi(df["Close"])
    return df
