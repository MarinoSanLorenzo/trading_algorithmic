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

    return information, stock_data

class TestInformation:

    def test_summary_strategy(self, inf_data:tuple):
        information, stock_data = inf_data


    def test_information_tbl(self, inf_data:tuple):
        information = inf_data, _
        stocks = list(params.get("STOCK_CODES").keys())
        for stock in stocks:
            assert stock in information.columns