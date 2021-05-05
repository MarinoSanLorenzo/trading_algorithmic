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

    ###########################################################
    #################        FRONT END                 #################
    ###########################################################

    open_prices_plot = plot(stock_data, y="Open")

    app = dash.Dash(__name__, external_stylesheets=params.get("STYLE_SHEET"))
    app.layout = get_layout(open_prices_plot, data["bitcoin"])
    app.run_server(debug=True)


if __name__ == "__main__":
    main()


# if __name__ == '__main__':
#     main()
