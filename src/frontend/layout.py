import dash_core_components as dcc
import dash_html_components as html
import plotly
import pandas as pd
import dash
from src.constants import params
from dash_main import app


def get_layout(params:dict  ) -> html.Div:
    layout = html.Div(
        children=[
            html.H1(children="Trading Dashboard"),
            dcc.Tabs(
                [
                    dcc.Tab(label='DEBUG'
                            ),

                    dcc.Tab(
                        label="Prices time series",
                        children=[
                            dcc.Dropdown(
                                id='chosen-stocks',
                                options=[
                                    {'label': stock, 'value':stock}
                                    for stock in params.get('STOCK_CODES')
                                ],
                                multi=True,
                                searchable=True,
                                value=list(params.get('STOCK_CODES').keys())
                            ),

                                dcc.Graph(figure=params.get('open_prices_plot')),
                                dcc.Graph(figure=params.get('bitcoin_low_high_plot')),
                                dcc.Graph(figure=params.get('ethereum_low_high_plot')),
                                dcc.Graph(figure=params.get('volume_plot')),

                                  ],

                    ),
                    dcc.Tab(
                        label="High-Low Price"

                    ),
                ]
            ),

        ]
    )

    return layout
