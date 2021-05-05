import datetime
from src.constants import params
import dash
from src.utils import *
from src.frontend.layout import *
from src.frontend.plots import *


def main():
    ###########################################################
    #################     BACKEND                    #################
    ###########################################################
    data = get_data(params, stocks=["bitcoin", "ethereum"])
    stock_data = stack_data(data)

    open_prices_plot = plot(stock_data, y="Open")

    ###########################################################
    #################        FRONT END                 #################
    ###########################################################
    app = dash.Dash(__name__, external_stylesheets=params.get("STYLE_SHEET"))
    app.layout = get_layout(open_prices_plot)

    app.run_server(debug=True)


if __name__ == "__main__":
    main()


# if __name__ == '__main__':
#     main()
