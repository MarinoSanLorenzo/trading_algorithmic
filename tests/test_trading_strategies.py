import pytest
import pandas as pd
import numpy as np
from talib import RSI, BBANDS

from src.utils import *
from src.constants import params
from src.trading_strategies import *

@pytest.fixture
def data() -> dict:
    data = get_data(params, stocks=["bitcoin", "ethereum"])
    return data


@pytest.fixture
def stock_data(data: dict) -> pd.DataFrame:
    for name, df in data.items():
        df["stock_name"] = name
        df["date"] = df.index
    stock_data = pd.concat([df for df in data.values()])
    stock_data["Total Traded"] = stock_data["Open"] * stock_data["Volume"]
    return stock_data

@pytest.fixture
def stock_data_ta(stock_data:pd.DataFrame) -> pd.DataFrame:
    stock_name = 'bitcoin'
    data = stock_data.query(f'stock_name=="{stock_name}"')
    close_prices = data['Adj Close'].values
    up, mid, low = BBANDS(close_prices, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    rsi = RSI(close_prices, timeperiod=14)
    bbp = (data['Adj Close'] - low) / (up - low)
    data['lower_bound'] = low
    data['up_bound'] = up
    data['RSI'] = rsi
    data['BBP'] = bbp
    return data

@pytest.fixture
def stock_data_tas(stock_data:pd.DataFrame) -> pd.DataFrame:
    datas=[]
    for stock_name in params.get('STOCK_CODES'):
        datas.append(get_technical_analysis(stock_data, stock_name))

    data = pd.concat(datas)
    return data

class TestTradingStrategy:

    def test_get_technical_analysis_all(self, stock_data:pd.DataFrame):
        data = get_technical_analysis_all(stock_data, params)
        assert 'lower_bound' in data.columns
        assert 'upper_bound' in data.columns
        assert 'RSI' in data.columns
        assert 'BBP' in data.columns
        assert data.shape[0]==stock_data.shape[0]

    def test_get_technical_analysis(self, stock_data:pd.DataFrame):
        stock_name='bitcoin'
        data = get_technical_analysis(stock_data, stock_name)
        assert 'lower_bound' in data.columns
        assert 'upper_bound' in data.columns
        assert 'RSI' in data.columns
        assert 'BBP' in data.columns



