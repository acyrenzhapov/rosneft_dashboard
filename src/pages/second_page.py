import plotly.express as px
import segyio
from dash import Input, Output, State, callback, dcc, html, register_page

from src.read_segy import get_segy_cube_shape

register_page(__name__)

layout = html.Div(
    [
        html.Div(id='my-output'),
    ],
    id='second-page-layout'
)


@callback(
    Output('my-output', 'children'),
    Input('intermediate-value', 'data'),
)
def get_store_data(data):
    return f'{data}'
