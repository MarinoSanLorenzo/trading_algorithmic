import pytest
import pandas as pd
from src.utils import *
from src.constants import params
from src.frontend.plots import *


@pytest.fixture
def data() -> dict:
    data = get_data(params, stocks=["bitcoin", "ethereum"])
    return data


@pytest.fixture
def stock_data(data: dict) -> pd.DataFrame:
    stock_data = stack_data(data)
    return stock_data


class TestPlots:
    def test_stack_data(self, stock_data: pd.DataFrame):
        open_prices_plot = plot(stock_data, y="Open")
        open_prices_plot.show()

    def test_plot_low_high_prices(self, data):
        name = "ethereum"
        ethereum = data[name]
        low_high_plot = plot_low_high_prices(ethereum, name)
        low_high_plot.show()
