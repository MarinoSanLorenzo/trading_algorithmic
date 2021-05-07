import datetime
from src.constants import params
import dash
from dash_main import *
from dash.dependencies import Input, Output

from src.utils import *
from src.frontend.layout import *
from src.frontend.plots import *
from src.frontend.callbacks import *

def main():
    ###########################################################
    #################     BACKEND                    #################
    ###########################################################
    stocks = list(params.get('STOCK_CODES').keys())
    data = get_data(params, stocks=["bitcoin", "ethereum"])
    stock_data = stack_data(data)





    ###########################################################
    #################        FRONT END                 #################
    ###########################################################

    params['open_prices_plot'] = plot(stock_data, y="Open", title='Open Prices')

    for stock in stocks:
        params[f'{stock}_low_high_plot'] = plot_low_high_prices(data[stock], stock)

    params['volume_plot'] = plot(stock_data, y="Volume", title='Volume traded')

    app.layout = get_layout(params)
    app.run_server(debug=True)






if __name__ == "__main__":
    main()

