import pandas as pd
import plotly.express as px
import plotly

__all__ = ["plot"]


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
