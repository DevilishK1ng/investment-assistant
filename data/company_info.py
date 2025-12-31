import yfinance as yf

def get_company_info(ticker: str) -> dict:
    stock = yf.Ticker(ticker)
    info = stock.info

    return {
        "name": info.get("longName", "N/A"),
        "sector": info.get("sector", "N/A"),
        "industry": info.get("industry", "N/A"),
        "market_cap": info.get("marketCap", None),
        "pe_ratio": info.get("trailingPE", None),
        "currency": info.get("currency", "USD")
    }
