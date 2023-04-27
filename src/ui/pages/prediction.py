import dash_bootstrap_components as dbc
from dash import dcc, html
from dash_labs.plugins import register_page


register_page(
    __name__,
)

controls = [
    dbc.Form(
        [
            dbc.Label(
                'Путь к сейсмическому кубу',
                className='mt-1',
            ),
            dbc.Input(
                id='segy-input',
                style={
                    'width': '100%',
                },
            ),
        ],
        id='segy-npz-path',
    ),
    dbc.Form(
        [
            dbc.Label(
                'Путь к нейронной сети',
                className='mt-1',
            ),
            dbc.Input(
                id='fault-mask-input',
                style={
                    'width': '100%',
                },
            ),
        ],
        id='fault-mask-path',
    ),
    dbc.Form(
        [
            dbc.Button(
                id='dataset-submit-button',
                n_clicks=0,
                children='Предсказать',
                color='secondary',
                size='sm',
                className='me-1 my-2',
            ),
        ],
    ),
]

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Card(controls, body=True),
            ],
        ),
        html.Div(id='div-placeholder')
    ],
)
