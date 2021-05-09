import pytest
import pandas as pd
from copy import deepcopy
from src.utils import *
from src.constants import params
from src.frontend.plots import *
from src.trading_strategies import *
from pandas.plotting import scatter_matrix
import plotly.figure_factory as ff
import plotly.express as px


@pytest.fixture
def stocks() -> dict:
    stocks = ["bitcoin", "ethereum"]
    return stocks


@pytest.fixture
def data() -> dict:
    data = get_data(params, stocks=["bitcoin", "ethereum"])
    return data


@pytest.fixture
def stock_data(data: dict) -> pd.DataFrame:
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
def stock_data_ma(stock_data: pd.DataFrame, stocks: list) -> pd.DataFrame:
    return get_moving_averages(stock_data, params)
    return stock_data_ma


@pytest.fixture
def stock_data_returns(stock_data: pd.DataFrame) -> pd.DataFrame:
    stock_data_returns = pd.concat(
        [get_return(stock_data, stock) for stock in params.get("STOCK_CODES")]
    )
    return stock_data_returns

@pytest.fixture
def stock_data_tas(stock_data:pd.DataFrame) -> pd.DataFrame:
    data = get_technical_analysis_all(stock_data, params)
    return data

class TestPlots:

    def test_cum_plots(self, stock_data:pd.DataFrame):
        fig = plot_cum_profits(stock_data, 'orders_ma_cum_profits', params)
        fig.show()

    def test_rsi_plot(self, stock_data_tas:pd.DataFrame ):
        fig = plot_rsi(stock_data_tas)
        fig.show()

    def test_bollinger_band_plot(self, stock_data_tas:pd.DataFrame):
        name = 'bitcoin'
        fig=plot_bollinger_bands(stock_data_tas, name)
        fig.show()

    def test_cum_return_plot(self, stock_data_returns:pd.DataFrame):
        cum_returns_plot = plot(stock_data_returns, y="cum_returns", title="Cumulative Returns")
        cum_returns_plot.show()

    def test_returns_scatter_matrix_plot(self, stock_data_returns: pd.DataFrame):
        returns_comp = pd.concat(
            [
                stock_data_returns.query(f'stock_name=="{stock}"')["returns"]
                for stock in params.get("STOCK_CODES")
            ], axis=1
        )
        returns_comp.columns = [
            f"{stock.capitalize()} returns" for stock in params.get("STOCK_CODES")
        ]
        fig = px.scatter_matrix(returns_comp)
        fig.show()

    def test_dist_returns_plots(self, stock_data_returns: pd.DataFrame):
        hist_data = [
            stock_data_returns.query(f'stock_name=="{stock}"')["returns"]
            for stock in params.get("STOCK_CODES")
        ]
        group_labels = [stock for stock in params.get("STOCK_CODES")]
        try:
            fig = ff.create_distplot(hist_data, group_labels, bin_size=0.01)
        except ValueError:
            for data in hist_data:
                data.dropna(inplace=True)
            fig = ff.create_distplot(hist_data, group_labels, bin_size=0.01)
        fig.show()

    def test_scatter_matrix_plot(self, data: pd.DataFrame):
        crypto_comp = pd.concat(
            [data[stock]["Open"] for stock in params.get("STOCK_CODES")], axis=1
        )
        crypto_comp.columns = [
            f"{stock.capitalize()} Open" for stock in params.get("STOCK_CODES")
        ]
        fig = px.scatter_matrix(crypto_comp)
        fig.show()

    def test_stack_data(self, stock_data: pd.DataFrame):
        open_prices_plot = plot(stock_data, y="Open", title="Open Prices")
        open_prices_plot.show()

    def test_plot_low_high_prices(self, data):
        name = "ethereum"
        ethereum = data[name]
        low_high_plot = plot_low_high_prices(ethereum, name)
        low_high_plot.show()

    def test_plot_volume(self, stock_data: pd.DataFrame):
        volume_plot = plot(stock_data, y="Volume", title="Volume traded")
        volume_plot.show()

    def test_plot_total_traded(self, stock_data: pd.DataFrame):
        total_traded_plot = plot(stock_data, y="Total Traded", title="Total Traded")
        total_traded_plot.show()

    def test_plot_moving_average(self, stock_data: pd.DataFrame):
        name = "ethereum"
        ethereum = stock_data.query(f'stock_name=="{name}"')
        ethereum_moving_average_plot = plot_moving_average(ethereum, name)
        ethereum_moving_average_plot.show()
        name = "bitcoin"
        bitcoin = stock_data.query(f'stock_name=="{name}"')
        bitcoin_moving_average_plot = plot_moving_average(bitcoin, name)
        bitcoin_moving_average_plot.show()
