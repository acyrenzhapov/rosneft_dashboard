import dash
import dash_bootstrap_components as dbc
import dash_labs as dl
from dash import dcc

from src.ui.tasks.segmentation_task import SegmentationTask

FONT_AWESOME = 'https://use.fontawesome.com/releases/v5.10.2/css/all.css'

app = dash.Dash(
    __name__,
    plugins=[dl.plugins.pages],
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        FONT_AWESOME,
    ]
)

navbar = dbc.NavbarSimple(
    [
        dbc.NavLink(
            page['name'],
            href=page['path'],
        ) for page in dash.page_registry.values()
    ],
    brand='Fault Segmentation',
    color='info',
    dark=True,
    className='mb-2 bg-dark',
)

store = dcc.Store(
    id='store',
    data={
        'segy_path': '../data/F3_Dip.sgy',
    },
),

app.layout = dbc.Container(
    [
        navbar,
        *store,
        dl.plugins.page_container,
    ],
    fluid=True,
)

if __name__ == '__main__':
    task = SegmentationTask()
    task.launch()
    app.run_server(debug=True)
