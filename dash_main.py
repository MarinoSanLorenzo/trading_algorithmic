import dash
from src.constants import params
from src.utils import *

__all__ = ['app']

app = dash.Dash(__name__, external_stylesheets=params.get("STYLE_SHEET"))

