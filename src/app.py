"""
This example demonstrates sharing data between pages of a multi-page app.
Note that dcc.Store is in the app.py file so that it's accessible to all pages.
"""


from dash import html, dcc
import dash_bootstrap_components as dbc
import dash
from dash_slicer import VolumeSlicer
import numpy as np
from src.read_segy import get_full_data

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=external_stylesheets,
)

cube = get_full_data('..\\data\\F3_Dip.sgy').T
spacing = 1, 1, 1

slicer0 = VolumeSlicer(app, cube, spacing=spacing, axis=2, thumbnail=False)
slicer1 = VolumeSlicer(app, cube, spacing=spacing, axis=1)

slicer0.graph.config["scrollZoom"] = False
slicer1.graph.config["scrollZoom"] = False

app.layout = html.Div(
    [
        html.H1("Multi Page App Demo: Sharing data between pages"),
        dbc.Nav(
            [
                dbc.NavLink(
                    html.Div(page["name"], className="ms-2"),
                    href=page["path"],
                    active="exact",
                )
                for page in dash.page_registry.values()
            ],
            pills=True,
        ),
        html.Div(
            [
                '../data/F3_Similarity.sgy',
                html.Br(),
                '../data/F3_Dip.sgy',
            ]
        ),
        html.Hr(),
        dcc.Store(
            id='intermediate-value',
            data={
                'segy_path': '../data/F3_Dip.sgy',
            },
        ),
        dash.page_container,
        html.Div([slicer0.graph, html.Br(), slicer0.slider, *slicer0.stores]),
        html.Div([slicer1.graph, html.Br(), slicer1.slider, *slicer1.stores]),
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True)
