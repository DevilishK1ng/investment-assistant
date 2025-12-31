def evaluate_signals(df):
    if df["RSI"].iloc[-1] < 30:
        return "Buen momento para comprar"
    if df["RSI"].iloc[-1] > 70:
        return "Buen momento para vender"
    return None
