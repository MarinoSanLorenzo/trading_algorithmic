import dash_core_components as dcc
import dash_html_components as html


def get_layout(fig):
    layout = html.Div(
        children=[
            html.H1(children="Trading Dashboard"),
            html.Div(
                children="""
            Two stocks graph
        """
            ),
            dcc.Graph(id="example-graph", figure=fig),
        ]
    )
    return layout
