import pandas as pd
from dash.dependencies import Input, Output
import dash_html_components as html
import dash
import plotly

from src.frontend.plots import plot
from src.constants import params
from src.utils import *
from dash_main import *


# @app.callback(
#     Output(component_id='selected_stocks_debug', component_property='children'),
#     Input(component_id='stock_inputs', component_property='value')
# )
# def get_selected_stocks_debug(input_value:list) -> list:
#     return f'{input_value}, type {type(input_value)}'
#
#
# @app.callback(
#     Output(component_id='selected_stocks', component_property='children'),
#     Input(component_id='stock_inputs', component_property='value')
# )
# def get_selected_stocks(input_value:list) -> list:
#     return input_value
#
#
# @app.callback(
#     Output("prices_plot", "figure"),
#     Input("selected_stocks", "value")
#
# )
# def plot_prices(selected_stocks:list)-> plotly.graph_objects.Figure:
#     stock_data_filtered = stock_data[stock_data.stock_name.isin(selected_stocks)]
#     return plot(stock_data_filtered, y="Open")
#
#
#
#
#
# @app.callback(
#     Output("high_low_price_plot", "children"), Input("year-slider", "value"),
#     Input("stock-data", "data")
#
# )
# def update_plot_low_high_prices(
#     value:int, df: pd.DataFrame
# ) -> plotly.graph_objects.Figure:
#     name = 'bitcoin'
#     filtered_df = df
#
#
#     fig = plot_low_high_prices(filtered_df, name)
#
#     fig.update_layout(transition_duration=500)
#
#     return fig
#
# @app.callback(
#     Output("prices_plot_debug", "children"),
#     Input("selected_stocks", "value")
#
# )
# def plot_prices_debug(selected_stocks:list)-> plotly.graph_objects.Figure:
#     stock_data_filtered = stock_data[stock_data.stock_name.isin(selected_stocks)]
#     return type(plot(stock_data_filtered, "Open"))
#
#
# @app.callback(
#     Output("prices_plot", "figure"),
#     Input("selected_stocks", "value")
#
# )
# def plot_prices(selected_stocks:list)-> plotly.graph_objects.Figure:
#     stock_data_filtered = stock_data[stock_data.stock_name.isin(selected_stocks)]
#     return plot(stock_data_filtered, y="Open")
