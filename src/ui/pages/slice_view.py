import dash_bootstrap_components as dbc
from dash import dcc
from dash_labs.plugins import register_page

import src.ui.callbacks.slice_view  # noqa: WPS301 F401

register_page(
    __name__,
)

segy_settings = [
    dbc.Form(
        [
            dbc.Label('Путь к seg-y файлу'),
            dbc.Input(
                id='segy-path-input',
                value='../data/F3_Similarity.sgy',
            ),
            dbc.Button(
                id='segy-path-submit-button',
                n_clicks=0,
                children='Загрузить датасет',
                color='secondary',
                size='sm',
                className='me-1 my-2',
            ),
        ],
    ),
]

slice_view_row = dbc.Card(
    [
        dbc.CardHeader('Срез сейсмического куба'),
        dbc.CardBody(
            [
                dcc.Graph(
                    id='div-example-graph',
                    style={
                        'height': '50vh',
                    },
                ),
                dcc.Slider(
                    value=0,
                    step=1,
                    id='slice-slider',
                    tooltip={'placement': 'bottom'},
                ),
            ],
        ),
        dbc.CardFooter(
            [
                dcc.Dropdown(
                    [
                        'xline',
                        'inline',
                    ],
                    value='xline',
                    id='perpendicular-way',
                    style={'width': '50%'},
                ),
                *segy_settings,
            ],
        ),
    ],
)

layout = dbc.Container(
    [
        dbc.Row(
            [
                slice_view_row,
            ],
        ),
    ],
)
