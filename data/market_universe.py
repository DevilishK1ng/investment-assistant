import pandas as pd
import requests
from io import StringIO

WIKI_SP500_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

def get_sp500_tickers():
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; InvestmentAssistant/1.0)"
    }

    response = requests.get(WIKI_SP500_URL, headers=headers, timeout=20)
    response.raise_for_status()

    html = response.text
    tables = pd.read_html(StringIO(html))

    df = tables[0]
    tickers = df["Symbol"].tolist()

    # Ajuste para Yahoo Finance (BRK.B → BRK-B)
    tickers = [t.replace(".", "-") for t in tickers]

    return tickers
