import pandas_datareader.data as web
import pandas as pd

__all__ = ["get_data", "stack_data", "get_date_max_min_volume_traded", "get_moving_average"]


def get_moving_average(stock_data:pd.DataFrame,stock_name:str, time_horizon:int) ->pd.DataFrame:
    data = stock_data.query(f'stock_name=="{stock_name}"')
    data[f'MA{time_horizon}'] = data['Open'].rolling(time_horizon).mean()
    return data

def get_date_max_min_volume_traded(stock_data:pd.DataFrame, stock_name:str) -> pd.DataFrame:
    data = stock_data.query(f'stock_name=="{stock_name}"')
    date_max_vol_traded = data.index[data['Total Traded'].argmax()]
    date_min_vol_traded = data.index[data['Total Traded'].argmin()]
    return pd.DataFrame.from_dict({'variable_name':['date_max_vol_traded','date_min_vol_traded'],
                                 stock_name:[date_max_vol_traded,date_min_vol_traded]})


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
