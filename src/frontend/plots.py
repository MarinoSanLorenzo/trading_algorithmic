import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly
from dash.dependencies import Input, Output
import dash
from src.constants import params
from dash_main import *

__all__ = ["plot", "plot_low_high_prices", "plot_moving_average"]




def plot(
    data: pd.DataFrame,
    y,
    title=None,
    x="date",
    label="stock_name",
    line_shape="spline",
    render_mode="svg",
) -> plotly.graph_objects.Figure:
    return px.line(
        data,
        x=x,
        y=y,
        title=title,
        color=label,
        line_group=label,
        hover_name=label,
        line_shape=line_shape,
        render_mode=render_mode,
    )


def add_trace_high_low(
    fig: plotly.graph_objects.Figure, df: pd.DataFrame
) -> plotly.graph_objects.Figure:

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df.High,
            name="High",
            line=dict(color="firebrick", width=1, dash="dash"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df.Low,
            name="Low",
            line=dict(color="royalblue", width=1, dash="dash"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df.index, y=df.Open, name="Open", line=dict(color="firebrick", width=1)
        )
    )
    return fig

def add_trace_moving_average(
    fig: plotly.graph_objects.Figure, df: pd.DataFrame
) -> plotly.graph_objects.Figure:

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df.MA50,
            name="MA50",
            line=dict(color="firebrick", width=1, dash="dash"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df.MA200,
            name="MA200",
            line=dict(color="royalblue", width=1, dash="dash"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df.index, y=df.Open, name="Open", line=dict(color="firebrick", width=1)
        )
    )
    return fig


def plot_low_high_prices(df: pd.DataFrame, name: str) -> plotly.graph_objects.Figure:

    fig = go.Figure()
    # Create and style traces
    fig = add_trace_high_low(fig, df)
    # Edit the layout
    fig.update_layout(
        title=f"Average High, Low and Open Prices for {name} stock",
        xaxis_title="Date",
        yaxis_title="Prices",
    )
    return fig

def plot_moving_average(df:pd.DataFrame, name: str)-> plotly.graph_objects.Figure:

    fig = go.Figure()
    # Create and style traces
    fig = add_trace_moving_average(fig, df)
    # Edit the layout
    fig.update_layout(
        title=f"Moving Average and Open for {name} stock",
        xaxis_title="Date",
        yaxis_title="Prices",
    )
    return fig