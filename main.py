import datetime
from src.constants import params
import dash
from dash_main import *
from dash.dependencies import Input, Output
import dash_table
from collections import defaultdict

from src.utils import *
from src.frontend.layout import *
from src.frontend.plots import *
from src.frontend.callbacks import *
from src.trading_strategies import *


params = get_user_inputs(params)

def main():

    ###########################################################
    #################     BACKEND                    #################
    ###########################################################

    # TODO:user input
    # risk measure

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
    all_strat_risk_measures = get_all_strategy_risk_measures(stock_data)


    params["information"] = information

    ###########################################################
    #################        FRONT END                 #################
    ###########################################################

    params["open_prices_plot"] = plot(stock_data, y="Open", title="Open Prices")

    high_low_plots_lst = []
    for stock in stocks:
        high_low_plots_lst.append(dcc.Graph(figure=plot_low_high_prices(data[stock], stock)) )
        high_low_plots_lst.append(html.Hr())
    params['high_low_plots_lst'] = high_low_plots_lst

    params["volume_plot"] = plot(stock_data, y="Volume", title="Volume traded")
    params["total_traded_plot"] = plot(
        stock_data, y="Total Traded", title="Total Traded"
    )

    params['moving_average_plots_lst'] = add_multiplots_components(stock_data, plot_moving_average)



    params["scatter_matrix_plot"] = plot_scatter_matrix(data, params)


    params["dist_returns_plots"] = plot_dist_returns(stock_data, params)
    params["returns_scatter_matrix_plot"] = plot_returns_scatter_matrix(stock_data, params)
    params["cum_return_plot"] = plot_cum_return(stock_data)
    params["rsi_plot"] = plot_rsi(stock_data)
    params['orders_ma_cum_profits_plot'] = plot_cum_profits(stock_data, 'orders_ma_cum_profits' ,params, 'MA')
    params['orders_bb_cum_profits_plot'] = plot_cum_profits(stock_data, 'orders_bb_cum_profits' ,params, 'BB')
    params['orders_rsi_cum_profits_plot'] = plot_cum_profits(stock_data, 'orders_rsi_cum_profits' ,params, 'RSI')


    params['bolliger_bans_plots_lst'] =  add_multiplots_components(stock_data, plot_bollinger_bands)
    params['all_strategy_risk_measures']  = get_data_table(all_strat_risk_measures)
    app.layout = get_layout(params)
    app.run_server(debug=True)


if __name__ == "__main__":
    main()
