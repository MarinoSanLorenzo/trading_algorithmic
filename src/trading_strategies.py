import pandas as pd
import numpy as np
from talib import RSI, BBANDS
from src.constants import params

__all__ = ['get_technical_analysis', 'get_technical_analysis_all']


def get_technical_analysis_all(stock_data:pd.DataFrame, params:dict) -> pd.DataFrame:
    return pd.concat([get_technical_analysis(stock_data, stock_name) for stock_name in params.get('STOCK_CODES')])


def get_technical_analysis(stock_data:pd.DataFrame, stock_name:str) -> pd.DataFrame:
    data = stock_data.query(f'stock_name=="{stock_name}"')
    close_prices = data['Adj Close'].values
    up, mid, low = BBANDS(close_prices, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    rsi = RSI(close_prices, timeperiod=14)
    bbp = (data['Adj Close'] - low) / (up - low)
    data['lower_bound'] = low
    data['upper_bound'] = up
    data['RSI'] = rsi
    data['BBP'] = bbp
    return data