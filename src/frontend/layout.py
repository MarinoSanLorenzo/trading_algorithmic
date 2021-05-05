import dash_core_components as dcc
import dash_html_components as html
import plotly
import pandas as pd


def get_layout(fig: plotly.graph_objects.Figure, df: pd.DataFrame) -> html.Div:
    dates_ordinal = [date.toordinal() for date in df.index]
    layout = html.Div(
        children=[
            html.H1(children="Trading Dashboard"),
            dcc.Tabs(
                [
                    dcc.Tab(
                        label="Prices time series",
                        children=[dcc.Graph(id="price_plot", figure=fig)],
                    ),
                    dcc.Tab(
                        label="High-Low Price",
                        children=[
                            dcc.Graph(id="price_plot2", figure=fig),
                            dcc.Slider(
                                id='year-slider',
                                min=min(dates_ordinal),
                                max=max(dates_ordinal),
                                value=min(dates_ordinal),
                                marks={str(year): str(year) for year in df.index.unique()},
                                step=None
                            )
                        ], dcc.Store(id='bitcoin-data')
                    ),
                ]
            ),#TODO: store data and finish slider + callback output input

        ]
    )
    periods = [i for i, _ in enumerate(df.index)]
    return layout
