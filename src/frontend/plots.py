import pandas as pd
from  copy import deepcopy
import plotly.express as px
import plotly.graph_objects as go
import plotly

import plotly.figure_factory as ff

__all__ = [
    "plot",
    "plot_low_high_prices",
    "plot_moving_average",
    "plot_scatter_matrix",
    "plot_dist_returns",
    "plot_returns_scatter_matrix",
    "plot_cum_return",
    "plot_bollinger_bands",
    "plot_rsi",
    "plot_cum_profits"
]





def plot_cum_profits(stock_data:pd.DataFrame, strategy_profit_name:str, params:dict,
                     title:str) -> plotly.graph_objects.Figure:
    profits = [stock_data.query(f'stock_name=="{stock}"')[[strategy_profit_name, 'stock_name']] for stock in
               params.get(
                   'STOCK_CODES')]
    profits_first = deepcopy(profits[0])
    indexes = profits_first.index
    for i, profit in enumerate(profits):
        if i > 0:
            profits_first[strategy_profit_name] += profit[strategy_profit_name]
    total_cum_profits = profits_first
    total_cum_profits_df = pd.DataFrame.from_dict({strategy_profit_name: total_cum_profits[strategy_profit_name],
                                                   'stock_name': ['Total Strategy Cumulative Profits' for _ in
                                                                  range(len(total_cum_profits))]})
    total_cum_profits_df.index = indexes
    cum_profits_data = pd.concat([total_cum_profits_df, *profits])
    cum_profits_data.reset_index(drop=False, inplace=True)
    return plot(cum_profits_data, x='Date', y=strategy_profit_name, title=f"Cumulative Profits generated by {title} " \
                                                                            "strategy")




def plot_rsi(stock_data: pd.DataFrame) -> plotly.graph_objects.Figure:
    return plot(stock_data, y="RSI", title="Relative Strength Index (RSI)")


def add_trace_bollinger_bands(
    fig: plotly.graph_objects.Figure, df: pd.DataFrame
) -> plotly.graph_objects.Figure:

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df.upper_bound,
            name="upper bound",
            line=dict(color="firebrick", width=1, dash="dash"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df.lower_bound,
            name="lower bound",
            line=dict(color="royalblue", width=1, dash="dash"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df.index, y=df.Close, name="Closed", line=dict(color="firebrick", width=1)
        )
    )
    return fig

def plot_bollinger_bands(df: pd.DataFrame, name: str) -> plotly.graph_objects.Figure:
    df = df.query(f'stock_name=="{name}"')
    fig = go.Figure()
    # Create and style traces
    fig = add_trace_bollinger_bands(fig, df)
    # Edit the layout
    fig.update_layout(
        title=f"Bollinger Bands and Close {name} stock",
        xaxis_title="Date",
        yaxis_title="Prices",
    )
    return fig

def plot_cum_return(stock_data_returns: pd.DataFrame) -> plotly.graph_objects.Figure:
    return plot(stock_data_returns, y="cum_returns", title="Cumulative Returns")

def plot_returns_scatter_matrix(stock_data_returns: pd.DataFrame, params:dict, title:str="Scatter Matrix for "
                                                                                        "returns")-> \
        plotly.graph_objects.Figure:
    returns_comp = pd.concat(
        [
            stock_data_returns.query(f'stock_name=="{stock}"')["returns"]
            for stock in params.get("STOCK_CODES")
        ], axis=1
    )
    returns_comp.columns = [
        f"{stock.capitalize()} returns" for stock in params.get("STOCK_CODES")
    ]
    return px.scatter_matrix(returns_comp, title=title)


def plot_dist_returns(
    stock_data_returns: pd.DataFrame,
    params: dict
) -> plotly.graph_objects.Figure:
    hist_data = [
        stock_data_returns.query(f'stock_name=="{stock}"')["returns"]
        for stock in params.get("STOCK_CODES")
    ]
    group_labels = [stock for stock in params.get("STOCK_CODES")]
    try:
        fig = ff.create_distplot(hist_data, group_labels, bin_size=0.01)
    except ValueError:
        for data in hist_data:
            data.dropna(inplace=True)
        fig = ff.create_distplot(hist_data, group_labels, bin_size=0.01)
    return fig


def plot_scatter_matrix(
    data: dict, params: dict, title="Scatter Matrix for Open Prices"
) -> plotly.graph_objects.Figure:
    # crypto_comp = pd.concat(
    #     [data[stock]["Open"] for stock in params.get("STOCK_CODES")], axis=1
    # )
    open_data_dic = {}
    for stock_name, df in data.items():
        open_price_name =f'{stock_name.capitalize()} Open'
        df.rename(columns={'Open':open_price_name}, inplace=True)
        df = df[~df.index.duplicated()]
        open_data_dic[open_price_name] = df

    comp = pd.concat(
        [df[open_price_name] for open_price_name, df in open_data_dic.items()], axis=1
    )
    # comp.columns = [
    #     f"{stock.capitalize()} Open" for stock in params.get("STOCK_CODES")
    # ]
    return px.scatter_matrix(comp, title=title)


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


def plot_moving_average(df: pd.DataFrame, name: str) -> plotly.graph_objects.Figure:

    df = df.query(f'stock_name=="{name}"')
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
