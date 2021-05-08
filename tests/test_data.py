import pytest
import pandas as pd
from copy import deepcopy
from collections import defaultdict

from src.utils import *
from src.constants import params


@pytest.fixture
def stocks() -> dict:
    selected_stocks = ["bitcoin", "ethereum"]
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
    stock_data["Total Traded"] = stock_data["Open"] * stock_data["Volume"]
    return stock_data


@pytest.fixture
def stock_data_filtered(stock_data: pd.DataFrame, stocks) -> pd.DataFrame:
    stock_data_filtered = stock_data[stock_data.stock_name.isin(selected_stocks)]
    return stock_data_filtered


@pytest.fixture
def information(stock_data: pd.DataFrame, stocks: list) -> pd.DataFrame:
    dates_vol_traded = [
        get_date_max_min_volume_traded(stock_data, stock) for stock in stocks
    ]
    information = pd.merge(*dates_vol_traded, on="variable_name")
    return information


@pytest.fixture
def moving_average(stock_data: pd.DataFrame) -> pd.DataFrame:
    stock_name = "bitcoin"
    time_horizon = 50
    data = stock_data.query(f'stock_name=="{stock_name}"')
    data[f"MA{time_horizon}"] = data["Open"].rolling(time_horizon).mean()
    return data


@pytest.fixture
def stock_data_ma(stock_data: pd.DataFrame, stocks) -> pd.DataFrame:
    time_horizons = [50, 200]
    stock_data_ma = deepcopy(stock_data)
    mas = defaultdict(list)
    for time_horizon in time_horizons:
        ma_name = f"MA{time_horizon}"
        for stock in stocks:
            df_ma_stock = get_moving_average(stock_data_ma, stock, time_horizon)
            mas[ma_name].append(df_ma_stock)
    df_ma_dic = {}
    for ma_name, df_ma_stock_lst in mas.items():
        df_ma_dic[ma_name] = pd.concat(df_ma_stock_lst)

    first_df_to_be_merged = list(df_ma_dic.values())[0]
    first_df_name = list(df_ma_dic.keys())[0]
    for df_name, df_ma in df_ma_dic.items():
        if df_name != first_df_name:
            first_df_to_be_merged = pd.merge(
                first_df_to_be_merged,
                df_ma[["stock_name", df_name]],
                on=["stock_name", "Date"],
            )
    stock_data_ma = first_df_to_be_merged
    return stock_data_ma


@pytest.fixture
def data_return(tock_data: pd.DataFrame) -> pd.DataFrame:
    stock_name = "bitcoin"
    data = stock_data.query(f'stock_name=="{stock_name}"')
    data["returns"] = data["Close"].pct_change(1)

    stock_name = "ethereum"
    data1 = stock_data.query(f'stock_name=="{stock_name}"')
    data1["returns"] = data1["Close"].pct_change(1)

    data_return = pd.concat([data, data1])
    return data_return


def stock_data_returns(stock_data: pd.DataFrame) -> pd.DataFrame:
    stock_data_returns = pd.concat(
        [get_return(stock_data, stock) for stock in params.get("STOCK_CODES")]
    )
    return stock_data_returns


class TestData:
    def test_get_stock_data_returns(self, stock_data: pd.DataFrame):
        stock_data_returns = get_stock_data_returns(stock_data, params)
        assert "returns" in stock_data_returns.columns
        assert stock_data_returns.shape[0] == stock_data.shape[0]

    def test_get_return(self, stock_data: pd.DataFrame):
        data_return = get_return(stock_data, "bitcoin")
        assert "returns" in data_return.columns

    def test_stack_data(self, data: dict):
        stock_data = stack_data(data)
        assert data["bitcoin"].shape[0] * 2 == stock_data.shape[0]
        assert all(col in stock_data.columns for col in ["stock_name", "date"])
        assert stock_data.equals(stock_data)

    def test_get_data(self, data: dict):
        assert isinstance(data, dict)
        assert data["bitcoin"].shape == data["ethereum"].shape

    def test_information(self, information: pd.DataFrame, stocks: list):
        cols = ["variable_name", *stocks]
        for col in information.columns:
            assert col in cols

    def test_moving_average(self, moving_average: pd.DataFrame) -> pd.DataFrame:
        assert "MA50" in moving_average.columns

    def test_get_moving_average(
        self, stock_data: pd.DataFrame, stocks: list
    ) -> pd.DataFrame:
        time_horizons = [50, 200]
        b_50_ma = get_moving_average(stock_data, stocks[0], time_horizons[0])
        b_200_ma = get_moving_average(stock_data, stocks[0], time_horizons[1])

        e_50_ma = get_moving_average(stock_data, stocks[1], time_horizons[0])
        e_200_ma = get_moving_average(stock_data, stocks[1], time_horizons[1])

        df_50 = pd.concat([b_50_ma, e_50_ma])
        df_200 = pd.concat([b_200_ma, e_200_ma])

        df = pd.merge(df_50, df_200[["stock_name", "MA200"]], on=["stock_name", "Date"])
