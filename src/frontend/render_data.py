import pandas as pd
from dash.dependencies import Input, Output
import dash
from src.constants import params
from src.utils import *


app = dash.Dash("__main__", external_stylesheets=params.get("STYLE_SHEET"))


@app.callback(Output("raw_data", "children"))
def data() -> dict:
    return get_data(params, stocks=["bitcoin", "ethereum"])


@app.callback(Output("stock-data", "children"), Input("raw_data", "data"))
def stock_data(data: dict) -> pd.DataFrame:
    return stack_data(data)


@app.callback(Output("stock_name", "children"), Input("name", "data"))
def stock_name(name: str) -> str:
    return "bitcoin"


@app.callback(
    Output("bitcoin-data", "children"),
    Input("raw_data", "data"),
    Input("stock_name", "data"),
)
def bitcoin_data(data: dict, stock_name: str) -> pd.DataFrame:
    return data[stock_name]
