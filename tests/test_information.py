import pytest
import pandas as pd
from src.constants import params
from src.utils import *
from src.trading_strategies import *

@pytest.fixture
def inf_data() -> tuple:
    stocks = list(params.get("STOCK_CODES").keys())
    data = get_data(params, stocks=["bitcoin", "ethereum"])
    stock_data = stack_data(data)
    stock_data["Total Traded"] = stock_data["Open"] * stock_data["Volume"]

    dates_vol_traded = [
        get_date_max_min_volume_traded(stock_data, stock) for stock in stocks
    ]
    information = pd.merge(*dates_vol_traded, on="variable_name")

    stock_data = get_moving_averages(stock_data, params)
    stock_data = get_stock_data_returns(stock_data, params)
    stock_data = get_technical_analysis_all(stock_data, params)
    stock_data = ma_trading(stock_data)
    inf_data = information, stock_data
    return inf_data

@pytest.fixture
def profits_data(inf_data:tuple) ->pd.DataFrame:
    information, stock_data = inf_data
    strategy_name = 'orders_ma_nb'
    stock_name = 'bitcoin'
    data = stock_data.query(f'stock_name=="{stock_name}"')
    cum_order_name = f'{strategy_name}_cum'
    data[cum_order_name] = data[strategy_name].cumsum()
    profits = data[cum_order_name] * data['cum_returns']
    cum_profits_name = f'{strategy_name[:-len("nb")]}_cum_profits'
    data[cum_profits_name] = profits
    return data

class TestInformation:

    def test_get_strategy_profits_all(self, inf_data:tuple):
        information, stock_data = inf_data
        data= pd.concat([get_strategy_profits(stock_data, stock, 'orders_ma_nb')for stock in params.get('STOCK_CODES')])
        assert 'orders_ma_cum_profits' in data.columns
        assert stock_data.shape[0] == data.shape[0]




    def test_get_strategy_profits(self, inf_data:tuple):
        information, stock_data = inf_data
        profits_data= get_strategy_profits(stock_data, 'bitcoin', 'orders_ma_nb')
        assert 'orders_ma_cum_profits' in profits_data.columns

    def test_information_tbl(self, inf_data:tuple):
        information, _ = inf_data
        stocks = list(params.get("STOCK_CODES").keys())
        for stock in stocks:
            assert stock in information.columns