import pandas as pd
import numpy as np
from talib import RSI, BBANDS
from src.constants import params

__all__ = ['get_technical_analysis', 'get_technical_analysis_all', 'ma_trading', 'convert_orders_signal_to_nb',
           'get_strategy_profits', 'get_strategy_profits_all']


def ma_trading(stock_data_tas:pd.DataFrame) ->pd.DataFrame:
    data = stock_data_tas
    condition = (data['MA50'] > data['MA200'],
                 data['MA50'] == data['MA200'],
                 data['MA50'] < data['MA200'])
    choices = ("buy",
               "hold",
               "sell")
    data['orders_ma_signal'] = np.select(condition, choices, default='hold')
    data = convert_orders_signal_to_nb(data,'orders_ma_signal')
    data = get_strategy_profits_all(data,'orders_ma_nb')
    return data

def get_strategy_profits_all(stock_data:pd.DataFrame, strategy_order_name:str) -> pd.DataFrame:
    return pd.concat([get_strategy_profits(stock_data, stock, strategy_order_name) for stock in params.get('STOCK_CODES')])

def get_strategy_profits(stock_data:pd.DataFrame, stock_name:str, strategy_name:str) ->pd.DataFrame:
    data = stock_data.query(f'stock_name=="{stock_name}"')
    cum_order_name = f'{strategy_name}_cum'
    data[cum_order_name] = data[strategy_name].cumsum()
    profits = data[cum_order_name] *data['cum_returns']
    cum_profits_name = f'{strategy_name[:-len("nb")]}cum_profits'
    data[cum_profits_name] = profits
    return data

def convert_orders_signal_to_nb(stock_data:pd.DataFrame, serie_name:str) -> pd.DataFrame:
    if set(('buy', 'hold', 'sell'))!= set(stock_data[serie_name].unique()):
        raise ValueError
    condition = (stock_data[serie_name] == 'buy',
                 stock_data[serie_name] == 'hold',
                 stock_data[serie_name] == 'sell'
                 )
    choices = (1,
                 0,
                 -1
                 )
    stock_data[f'{serie_name[:-(len("signal"))]}nb'] = np.select(condition, choices)
    return stock_data

def get_technical_analysis_all(stock_data:pd.DataFrame, params:dict) -> pd.DataFrame:
    return pd.concat([get_technical_analysis(stock_data, stock_name) for stock_name in params.get('STOCK_CODES')])


def get_technical_analysis(stock_data:pd.DataFrame, stock_name:str) -> pd.DataFrame:
    data = stock_data.query(f'stock_name=="{stock_name}"')
    close_prices = data['Adj Close'].values
    up, mid, low = BBANDS(close_prices, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    rsi = RSI(close_prices, timeperiod=14)
    bbp = (data['Adj Close'] - low) / (up - low)
    data['lower_bound'] = low
    data['upper_bound'] = up
    data['RSI'] = rsi
    data['BBP'] = bbp
    return data