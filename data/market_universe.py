import pandas as pd

def get_sp500_tickers():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tables = pd.read_html(url)
    df = tables[0]
    return df["Symbol"].tolist()


import pandas as pd

def get_sp500_tickers():
    """
    Retorna la lista de tickers del S&P 500.
    Fuente: Wikipedia (estable y suficiente para uso diario).
    """
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tables = pd.read_html(url)
    df = tables[0]

    tickers = df["Symbol"].tolist()
    return tickers
