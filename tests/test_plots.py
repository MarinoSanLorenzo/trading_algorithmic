import pytest
import pandas as pd
from src.utils import *
from src.constants import params
from src.frontend.plots import *

@pytest.fixture
def stocks() -> dict:
    stocks=['bitcoin', 'ethereum']
    return stocks


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
    stock_data['Total Traded'] = stock_data['Open'] * stock_data['Volume']
    return stock_data

@pytest.fixture
def stock_data_ma(stock_data: pd.DataFrame, stocks:list) -> pd.DataFrame:

    for stock in stocks:
        data = stock_data[stock_data.stock_name==stock]
        data['MA50'] = data['Open'].rolling(50).mean()
        data['MA200'] = data['Open'].rolling(200).mean()
        stock_data_ma = pd.merge(stock_data, data[['MA50', 'MA200', 'stock_name']],how='left', on=['stock_name', 'Date'])
    return stock_data_ma

class TestPlots:
    def test_stack_data(self, stock_data: pd.DataFrame):
        open_prices_plot = plot(stock_data, y="Open", title='Open Prices')
        open_prices_plot.show()

    def test_plot_low_high_prices(self, data):
        name = "ethereum"
        ethereum = data[name]
        low_high_plot = plot_low_high_prices(ethereum, name)
        low_high_plot.show()


    def test_plot_volume(self, stock_data: pd.DataFrame):
        volume_plot = plot(stock_data, y="Volume", title='Volume traded')
        volume_plot.show()

    def test_plot_total_traded(self, stock_data: pd.DataFrame):
        total_traded_plot = plot(stock_data, y="Total Traded", title='Total Traded')
        total_traded_plot.show()

    def test_plot_moving_average(self, stock_data_ma: pd.DataFrame):
        name = "ethereum"
        ethereum = stock_data_ma.query(f'stock_name=="{name}"')
        moving_average_plot = plot_moving_average(ethereum, name)
        moving_average_plot.show()