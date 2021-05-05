import pytest
import pandas as pd
from src.utils import *
from src.constants import params


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
    return stock_data


class TestData:
    def test_stack_data(self, data: dict):
        stock_data = stack_data(data)
        assert data["bitcoin"].shape[0] * 2 == stock_data.shape[0]
        assert all(col in stock_data.columns for col in ["stock_name", "date"])
        assert stock_data.equals(stock_data)

    def test_get_data(self, data: dict):
        assert isinstance(data, dict)
        assert data["bitcoin"].shape == data["ethereum"].shape
