import pytest
import pandas as pd
import numpy as np
from collections import defaultdict
from statistics import *
from scipy.stats import *
from math import *
from scipy.optimize import *
from talib import RSI, BBANDS
from copy import deepcopy
from src.utils import *
from src.constants import params
from src.trading_strategies import *

@pytest.fixture
def stock_data():
    stocks = params.get("chosen_stocks")
    data = get_data(params, stocks=stocks)
    stock_data = stack_data(data)
    stock_data["Total Traded"] = stock_data["Open"] * stock_data["Volume"]

    dates_vol_traded = [
        get_date_max_min_volume_traded(stock_data, stock) for stock in stocks
    ]
    information = dates_vol_traded[0]
    for i in range(1, len(dates_vol_traded)):
        information = pd.merge(information, dates_vol_traded[i],  on="variable_name")


    stock_data = get_moving_averages(stock_data, params)
    stock_data = get_stock_data_returns(stock_data, params)
    stock_data = get_technical_analysis_all(stock_data, params)
    stock_data = ma_trading(stock_data)
    stock_data = bollinger_bands_trading(stock_data)
    stock_data = rsi_trading(stock_data)


    count_orders = get_count_orders_all_strat(stock_data, params)
    information = pd.concat([information, count_orders])
    return stock_data

@pytest.fixture
def stock_data_trading_ma(stock_data_tas: pd.DataFrame) -> pd.DataFrame:
    data = stock_data_tas
    condition = (data['MA50'] > data['MA200'],
                 data['MA50'] == data['MA200'],
                 data['MA50'] < data['MA200'])
    choices = ("buy",
               "hold",
               "sell")
    data['orders_ma_signal'] = np.select(condition, choices, default='hold')
    return data


@pytest.fixture
def total_cum_profits_df(stock_data:pd.DataFrame) -> pd.DataFrame:
    strategy_profit_name = 'orders_ma_cum_profits'
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

@pytest.fixture
def profit_and_losses(stock_data:pd.DataFrame) -> pd.Series:
    strategy_profit_name = 'orders_ma_cum_profits'
    total_cum_profits_df = get_total_cum_profits(stock_data, strategy_profit_name)
    profit_and_losses = total_cum_profits_df.orders_ma_cum_profits.diff()
    return profit_and_losses

@pytest.fixture
def risk_var(stock_data:pd.DataFrame) -> float:
        quantile_lvl = 0.05
        strategy_profit_name = 'orders_ma_cum_profits'
        profit_and_losses = get_profit_and_losses(stock_data, strategy_profit_name)
        losses = profit_and_losses[profit_and_losses<0]
        var_lvl = losses.quantile(quantile_lvl)
        return var_lvl


@pytest.fixture
def risk_measures(stock_data:pd.DataFrame) -> RiskMeasures:
    strategy_profit_name = 'orders_ma_cum_profits'
    def obj_fct(VaR, z):
        alpha = 0.01;
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
    risk_measures  = RiskMeasures(empiric_var, GaussianVaR, GaussianES, NonParamVaR, NonParamES, losses)
    return risk_measures

@pytest.fixture
def all_strategy_risk_measures(stock_data:pd.DataFrame) -> pd.DataFrame:
    strategy_risk_measures_dic = {'MA':'orders_ma_cum_profits',"BB": 'orders_bb_cum_profits',
                                  'RSI' :'orders_rsi_cum_profits'}
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
class TestTradingStrategy:

    def test_get_all_strategy_risk_measures(self, stock_data:pd.DataFrame) -> None:
        strategy_risk_measures_dic = {'MA': 'orders_ma_cum_profits', "BB": 'orders_bb_cum_profits',
                                      'RSI': 'orders_rsi_cum_profits'}
        all_strategy_risk_measures = get_all_strategy_risk_measures(stock_data)
        for col in all_strategy_risk_measures.columns:
            assert col in strategy_risk_measures_dic.keys()

        for col in all_strategy_risk_measures.index:
            assert col in RiskMeasures._fields

    def test_get_risk_measure(self, stock_data:pd.DataFrame) -> None:
        strategy_profit_name = 'orders_ma_cum_profits'
        risk_measures = get_risk_measures(stock_data, strategy_profit_name)
        assert isinstance(risk_measures, RiskMeasures),f'{type(risk_measures)}'
        assert isinstance(risk_measures.losses, pd.Series),f'{type(risk_measures.losses)}'
        for field in risk_measures._fields:
            if field!='losses':
                risk_measure = getattr(risk_measures, field)
                assert isinstance(risk_measure, float),f'{field}:\t{type(risk_measure)}'

    def test_empiric_var(self, stock_data) -> None:
        strategy_profit_name = 'orders_ma_cum_profits'
        empiric_var = get_empiric_var(stock_data, strategy_profit_name)
        assert empiric_var <0
        assert isinstance(empiric_var, float)

    def test_get_profit_and_losses(self, stock_data:pd.DataFrame, total_cum_profits_df:pd.DataFrame) -> None:
        strategy_profit_name = 'orders_ma_cum_profits'
        profit_and_losses = get_profit_and_losses(stock_data, strategy_profit_name)
        assert isinstance(profit_and_losses, pd.Series)
        assert total_cum_profits_df.shape[0] ==profit_and_losses.shape[0]

    def test_get_total_cum_profits(self, stock_data:pd.DataFrame) -> None:
        strategy_profit_name = 'orders_ma_cum_profits'
        total_cum_profits_df = get_total_cum_profits(stock_data, strategy_profit_name)
        assert list(total_cum_profits_df.stock_name.unique())[0]== 'Total Strategy Cumulative Profits'

    def test_trading_ma(self, stock_data:pd.DataFrame):
        assert 'orders_ma_signal' in stock_data.columns
        assert 'orders_ma_nb' in stock_data.columns
        assert 'orders_ma_cum_profits' in stock_data.columns

    def test_convert_orders_signal_to_nb(self, stock_data:pd.DataFrame):
        assert 'orders_ma_nb' in stock_data.columns

    def test_trading_strategy_ma(self, stock_data:pd.DataFrame) -> pd.DataFrame:
        assert 'orders_ma_signal' in stock_data.columns




    def test_get_technical_analysis_all(self, stock_data:pd.DataFrame):
        data = get_technical_analysis_all(stock_data, params)
        assert 'lower_bound' in data.columns
        assert 'upper_bound' in data.columns
        assert 'RSI' in data.columns
        assert 'BBP' in data.columns
        assert data.shape[0]==stock_data.shape[0]

    def test_get_technical_analysis(self, stock_data:pd.DataFrame):
        stock_name='bitcoin'
        data = get_technical_analysis(stock_data, stock_name)
        assert 'lower_bound' in data.columns
        assert 'upper_bound' in data.columns
        assert 'RSI' in data.columns
        assert 'BBP' in data.columns



