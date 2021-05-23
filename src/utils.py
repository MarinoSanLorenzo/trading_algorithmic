import pandas_datareader.data as web
import numpy as np
import pandas as pd
from collections import defaultdict
from copy import deepcopy
from types import FunctionType

import dash_html_components as html
import dash_core_components as dcc

__all__ = [
    "get_data",
    "stack_data",
    "get_date_max_min_volume_traded",
    "get_moving_average",
    "get_moving_averages",
    "get_return",
    "get_stock_data_returns",
    "get_count_orders",
    "get_count_orders_all",
    "get_count_orders_all_strat",
    'add_multiplots_components'
]

def add_multiplots_components(stock_data:pd.DataFrame, plot_func:FunctionType) -> list:
    plots_lst = []
    stocks = list(stock_data.stock_name.unique())
    for stock in stocks:
        plots_lst.append(dcc.Graph(figure=plot_func(stock_data, stock)))
        plots_lst.append(html.Hr())
    return plots_lst

def get_count_orders_all_strat(stock_data:pd.DataFrame, params:dict) -> pd.DataFrame:
    strategies = ['orders_ma_signal', 'orders_bb_signal', 'orders_rsi_signal']
    return pd.concat([get_count_orders_all(stock_data, s, params) for s in strategies])



def get_count_orders_all(stock_data:pd.DataFrame, strategy_name:str, params:dict) -> pd.DataFrame:
    for i, stock in enumerate(params.get('STOCK_CODES')):
        if i == 0:
            data_basis = get_count_orders(stock_data, stock, strategy_name)
        if i > 0:
            data = get_count_orders(stock_data, stock, strategy_name)
            data_basis = pd.merge(data_basis, data, how='left', on='variable_name')
    return data_basis

def get_count_orders(stock_data:pd.DataFrame, stock_name:str, orders_name:str) -> pd.DataFrame:
    order_strat_name = f'{orders_name[:-len("signal")]}strategy'
    data = stock_data.query(f'stock_name=="{stock_name}"')
    count = getattr(data, orders_name).value_counts()
    variable_names = [f'{idx}_{order_strat_name}' for idx in count.index]
    return pd.DataFrame.from_dict({'variable_name': variable_names, stock_name: count.values})

def get_stock_data_returns(stock_data: pd.DataFrame, params: dict) -> pd.DataFrame:
    stock_data_returns = pd.concat(
        [get_return(stock_data, stock) for stock in params.get("STOCK_CODES")]
    )
    return stock_data_returns


def get_return(stock_data: pd.DataFrame, stock_name: str) -> pd.DataFrame:
    data = stock_data.query(f'stock_name=="{stock_name}"')
    data["returns"] = data["Close"].pct_change(1)
    data["cum_returns"] = (1 + data["returns"]).cumprod()
    return data


def get_moving_averages(
    stock_data: pd.DataFrame, params: dict, time_horizons: list = [50, 200]
) -> pd.DataFrame:
    stocks = list(params.get("STOCK_CODES").keys())
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


def get_moving_average(
    stock_data: pd.DataFrame, stock_name: str, time_horizon: int
) -> pd.DataFrame:
    data = stock_data.query(f'stock_name=="{stock_name}"')
    data[f"MA{time_horizon}"] = data["Open"].rolling(time_horizon).mean()
    return data


def get_date_max_min_volume_traded(
    stock_data: pd.DataFrame, stock_name: str
) -> pd.DataFrame:
    data = stock_data.query(f'stock_name=="{stock_name}"')
    date_max_vol_traded = data.index[data["Total Traded"].argmax()]
    date_min_vol_traded = data.index[data["Total Traded"].argmin()]
    return pd.DataFrame.from_dict(
        {
            "variable_name": ["date_max_vol_traded", "date_min_vol_traded"],
            stock_name: [date_max_vol_traded, date_min_vol_traded],
        }
    )


def stack_data(data: dict) -> pd.DataFrame:
    """
    Stack all the data into single dataframe
    :param data:
    :return:
    """
    for name, df in data.items():
        df["stock_name"] = name
        df["date"] = df.index
    return pd.concat([df for df in data.values()])


def get_data(params: dict, stocks: list) -> dict:
    """
    Fetch the data
    :param params:
    :param stocks: list of the selected stocks
    :return: dictionary with the dataframe as value per key stock
    """
    stock_codes = params.get("STOCK_CODES")
    start = params.get("START_DATE")
    end = params.get("END_DATE")
    data = {}
    for name, code in stock_codes.items():
        if name in stocks:
            data[name] = web.get_data_yahoo(code, start=start, end=end)
    return data
