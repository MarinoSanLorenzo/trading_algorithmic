import pandas as pd
import numpy as np
from talib import RSI, BBANDS
from copy import deepcopy
from collections import defaultdict
from src.constants import params
from statistics import *
from scipy.stats import *
from math import *
from scipy.optimize import *
from collections import namedtuple


__all__ = ['get_technical_analysis', 'get_technical_analysis_all', 'ma_trading', 'convert_orders_signal_to_nb',
           'get_strategy_profits', 'get_strategy_profits_all', 'bollinger_bands_trading', 'rsi_trading',
           'get_total_cum_profits', 'get_profit_and_losses', 'get_empiric_var', 'get_risk_measures',  'RiskMeasures', 'get_all_strategy_risk_measures']

RiskMeasures = namedtuple('RiskMeasures', 'empiric_var gaussian_var guassian_es non_parameter_var non_parameter_es '
                                          'losses')


def get_all_strategy_risk_measures(stock_data:pd.DataFrame,     strategy_risk_measures_dic:dict = {
    'MA':'orders_ma_cum_profits',"BB": 'orders_bb_cum_profits',
                                  'RSI' :'orders_rsi_cum_profits'})-> pd.DataFrame:

    risk_measures_dic = {strategy:get_risk_measures(stock_data, strategy_losses) for strategy, strategy_losses in
                         strategy_risk_measures_dic.items()}
    d = defaultdict(list)
    for strategy, risk_measure in risk_measures_dic.items():
        for field in risk_measure._fields:
            if field!='losses':
                d[strategy].append(getattr(risk_measure, field))
    df = pd.DataFrame.from_dict(d)
    df.index = [field for field in risk_measure._fields if field!='losses']
    return df

def get_empiric_var(stock_data:pd.DataFrame, strategy_profit_name:str, lvl:float=0.01) -> float:
    profit_and_losses = get_profit_and_losses(stock_data, strategy_profit_name)
    losses = profit_and_losses[profit_and_losses < 0]
    return losses.quantile(lvl)

def get_risk_measures(stock_data:pd.DataFrame, strategy_profit_name:str, alpha:float=0.01):
    def obj_fct(VaR, z):
        alpha=0.01
        h = np.std(z, ddof=1) * len(z) ** (-0.2)
        f = np.power(mean(norm.cdf((z - VaR) / h)) - alpha, 2)
        return f

    empiric_var = get_empiric_var(stock_data, strategy_profit_name)
    profit_and_losses = get_profit_and_losses(stock_data, strategy_profit_name)
    losses = profit_and_losses[profit_and_losses < 0]
    mu = np.mean(losses)
    sigma = np.std(losses, ddof=1)
    z_99 = norm.ppf(1 - alpha, 0, 1)  # obtain the extreme 99# quantile of loss
    GaussianVaR = mu + sigma * z_99
    GaussianES = mu + sigma * norm.pdf(z_99, 0, 1) / alpha
    NonParamVaR = fmin(func=obj_fct, x0=GaussianVaR, args=(losses,), disp=False)
    h = np.std(losses, ddof=1) * len(losses) ** (-0.2)
    NonParamES = mean(losses * norm.cdf((losses - NonParamVaR) / h)) / alpha
    return RiskMeasures(empiric_var, GaussianVaR, GaussianES, NonParamVaR[0], NonParamES, losses)




def get_profit_and_losses(stock_data:pd.DataFrame, strategy_profit_name:str) -> pd.Series:
    total_cum_profits_df = get_total_cum_profits(stock_data, strategy_profit_name)
    profit_and_losses = getattr(total_cum_profits_df, strategy_profit_name).diff()
    return profit_and_losses


def get_total_cum_profits(stock_data:pd.DataFrame, strategy_profit_name:str) -> pd.DataFrame:
    profits = [stock_data.query(f'stock_name=="{stock}"')[[strategy_profit_name, 'stock_name']] for stock in
               params.get(
                   'STOCK_CODES')]
    total_cum_profits = deepcopy(profits[0])
    total_cum_profits = total_cum_profits[~total_cum_profits.index.duplicated()]
    indexes = total_cum_profits.index
    for i in range(1,len(profits)):
            profits_stock = profits[i]
            profits_stock = profits_stock[~profits_stock.index.duplicated()]
            total_cum_profits[strategy_profit_name] += profits_stock[strategy_profit_name]

    total_cum_profits_df = pd.DataFrame.from_dict({strategy_profit_name: total_cum_profits[strategy_profit_name],
                                                   'stock_name': ['Total Strategy Cumulative Profits' for _ in
                                                                  range(len(total_cum_profits))]})

    total_cum_profits_df.index = indexes
    return total_cum_profits_df

def rsi_trading(data:pd.DataFrame) ->pd.DataFrame:
    condition = (data['RSI'] > 30,
                 data['RSI'] < 70)
    choices = ("buy",
               "sell")

    data['orders_rsi_signal'] = np.select(condition, choices, default='hold')
    data = convert_orders_signal_to_nb(data,'orders_rsi_signal')
    data = get_strategy_profits_all(data,'orders_rsi_nb')
    return data

def bollinger_bands_trading(data:pd.DataFrame) ->pd.DataFrame:
    condition = (data['lower_bound'] < data['Open'],
                 data['upper_bound'] > data['Open'])
    choices = ("buy",
               "sell")

    data['orders_bb_signal'] = np.select(condition, choices, default='hold')
    data = convert_orders_signal_to_nb(data,'orders_bb_signal')
    data = get_strategy_profits_all(data,'orders_bb_nb')
    return data

def ma_trading(data:pd.DataFrame) ->pd.DataFrame:
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
    # if set(('buy', 'hold', 'sell'))!= set(stock_data[serie_name].unique()):
    #     raise ValueError
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