import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly
from dash.dependencies import Input, Output
import dash
from src.constants import params

__all__ = ["plot", "plot_low_high_prices", "update_plot_low_high_prices"]

app = dash.Dash("__main__", external_stylesheets=params.get("STYLE_SHEET"))


@app.callback(
    Output("price_plot", "figure"), Input("year-slider", "value"),
)
def update_plot_low_high_prices(
    selected_year, df: pd.DataFrame, name: str
) -> plotly.graph_objects.Figure:
    filtered_df = df[df.date >= selected_year]

    fig = plot_low_high_prices(filtered_df, name)

    fig.update_layout(transition_duration=500)

    return fig


def plot(
    data: pd.DataFrame,
    y,
    x="date",
    label="stock_name",
    line_shape="spline",
    render_mode="svg",
) -> plotly.graph_objects.Figure:
    return px.line(
        data,
        x=x,
        y=y,
        color=label,
        line_group=label,
        hover_name=label,
        line_shape=line_shape,
        render_mode=render_mode,
    )


def add_trace(
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


def plot_low_high_prices(df: pd.DataFrame, name: str) -> plotly.graph_objects.Figure:

    fig = go.Figure()
    # Create and style traces
    fig = add_trace(fig, df)
    # Edit the layout
    fig.update_layout(
        title=f"Average High, Low and Open Prices for {name} stock",
        xaxis_title="Date",
        yaxis_title="Prices",
    )
    return fig
