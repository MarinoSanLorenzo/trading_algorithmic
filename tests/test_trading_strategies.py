import pytest
import pandas as pd
import numpy as np
from talib import RSI, BBANDS

from src.utils import *
from src.constants import params
from src.trading_strategies import *

@pytest.fixture
def stock_data():
    stocks = list(params.get("STOCK_CODES").keys())
    data = get_data(params, stocks=["bitcoin", "ethereum"])
    stock_data = stack_data(data)
    stock_data["Total Traded"] = stock_data["Open"] * stock_data["Volume"]

    stock_data = get_moving_averages(stock_data, params)
    stock_data = get_stock_data_returns(stock_data, params)
    stock_data = get_technical_analysis_all(stock_data, params)
    stock_data = ma_trading(stock_data)
    return stock_data

@pytest.fixture
def stock_data_trading_ma(self, stock_data_tas: pd.DataFrame) -> pd.DataFrame:
    data = stock_data_tas
    condition = (data['MA50'] > data['MA200'],
                 data['MA50'] == data['MA200'],
                 data['MA50'] < data['MA200'])
    choices = ("buy",
               "hold",
               "sell")
    data['orders_ma_signal'] = np.select(condition, choices, default='hold')
    return data


class TestTradingStrategy:

    def test_trading_ma(self, stock_data:pd.DataFrame):
        assert 'orders_ma_signal' in stock_data.columns
        assert 'orders_ma_nb' in stock_data.columns
        assert 'orders_ma_cum_profits' in stock_data.columns

    def test_convert_orders_signal_to_nb(self, stock_data:pd.DataFrame):
        assert 'orders_ma_nb' in stock_data.columns

    def test_trading_strategy_ma(self, stock_data:pd.DataFrame) -> pd.DataFrame:
        assert 'orders_ma_signal' in stock_data.columns




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



