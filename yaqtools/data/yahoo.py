from typing import List

import pandas as pd
import yfinance as yf


def get_sector_tickers(sectors: List):
    """
    Function to get top company symbol/tickers from Yahoo finance according to a list of sectors
    Parameters
    ----------
    sectors: list of sectors

    Returns
    -------

    """

    if isinstance(sectors, str):
        sectors = [sectors]

    dfs = []
    for sector in sectors:
        df = yf.Sector(sector).top_companies
        df["sector"] = sector
        dfs.append(df)

    df_sectors = pd.concat(dfs)

    return df_sectors
