import dash_core_components as dcc
import dash_html_components as html
import plotly
import pandas as pd
import dash
from src.constants import params
from dash_main import app
import dash_table


def get_layout(params: dict) -> html.Div:
    layout = html.Div(
        children=[
            html.H1(children="Trading Dashboard"),
            dcc.Tabs(
                [
                    dcc.Tab(label="DEBUG"),
                    dcc.Tab(
                        label="Prices time series",
                        children=[
                            dcc.Dropdown(
                                id="chosen-stocks",
                                options=[
                                    {"label": stock, "value": stock}
                                    for stock in params.get("STOCK_CODES")
                                ],
                                multi=True,
                                searchable=True,
                                value=list(params.get("STOCK_CODES").keys()),
                            ),
                            dcc.Graph(figure=params.get("open_prices_plot")),
                            *params.get('high_low_plots_lst'),
                            dcc.Graph(figure=params.get("volume_plot")),
                            dcc.Graph(figure=params.get("total_traded_plot")),
                            *params.get('moving_average_plots_lst'),
                            dcc.Graph(figure=params.get("scatter_matrix_plot")),
                            html.Div('Distribution of Returns'),
                            dcc.Graph(figure=params.get("dist_returns_plots")),
                            dcc.Graph(figure=params.get("returns_scatter_matrix_plot")),
                            dcc.Graph(figure=params.get("cum_return_plot")),
                        ],
                    ),
                    dcc.Tab(label='Trading analysis',
                            children=[
                                *params.get('moving_average_plots_lst'),
                                *params.get('bolliger_bans_plots_lst'),
                            dcc.Graph(figure=params.get("rsi_plot")),
                             dcc.Graph(figure=params.get("orders_ma_cum_profits_plot")),
                            dcc.Graph(figure=params.get("orders_bb_cum_profits_plot")),
                            dcc.Graph(figure=params.get("orders_rsi_cum_profits_plot")),
                            ]),
                    dcc.Tab(
                        label="Some information",
                        children=[
                            dash_table.DataTable(
                                columns=[
                                    {"name": i, "id": i}
                                    for i in params.get("information").columns
                                ],
                                data=params.get("information").to_dict("records"),

                            ),
                            html.Hr(),
                            html.Div('We present here some risk measures for all trading strategies'),
                            params.get('all_strategy_risk_measures')
                        ],
                    ),
                ]
            ),
        ]
    )

    return layout
