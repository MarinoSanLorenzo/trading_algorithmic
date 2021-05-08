import pytest
import pandas as pd
from src.utils import *
from src.constants import params


@pytest.fixture
def selected_stocks() -> dict:
    selected_stocks=['bitcoin', 'ethereum']
    return selected_stocks

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
def stock_data_filtered(stock_data: pd.DataFrame, selected_stocks:list) -> pd.DataFrame:
    stock_data_filtered = stock_data[stock_data.stock_name.isin(selected_stocks)]
    return stock_data_filtered


@pytest.fixture
def data_vol_traded(stock_data: pd.DataFrame):
    data = stock_data.query(f'stock_name=="bitcoin"')
    date_max_vol_traded = data.index[data['Total Traded'].argmax()]
    date_min_vol_traded = data.index[data['Total Traded'].argmin()]
    date_vol_traded =pd.DataFrame.from_dict({'variable_name': ['date_max_vol_traded', 'date_min_vol_traded'],
                            'bitcoin': [date_max_vol_traded, date_min_vol_traded]})


class TestData:
    def test_stack_data(self, data: dict):
        stock_data = stack_data(data)
        assert data["bitcoin"].shape[0] * 2 == stock_data.shape[0]
        assert all(col in stock_data.columns for col in ["stock_name", "date"])
        assert stock_data.equals(stock_data)

    def test_get_data(self, data: dict):
        assert isinstance(data, dict)
        assert data["bitcoin"].shape == data["ethereum"].shape


