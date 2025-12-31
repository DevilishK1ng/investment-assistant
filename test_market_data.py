from data.market_data import get_stock_data

df = get_stock_data("AAPL")

print(df.tail())
