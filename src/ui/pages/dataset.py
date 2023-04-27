import dash_bootstrap_components as dbc
from dash import dcc, html
from dash_labs.plugins import register_page


# register_page(
#     __name__,
# )

controls = [
    dbc.Form(
        [
            dbc.Label(
                'Размер датасета',
                className='mt-1',
            ),
            dbc.Input(
                id='dataset-size',
                type='number',
                step=1,
                value=100,
            ),
        ],
    ),
    dbc.Form(
        [
            dbc.Col(
                [
                    dbc.Label(
                        'Размер сейсмического куба',
                        className='col-mt-2',
                    ),
                    dbc.Input(
                        id='dataset-cube-size-2',
                        type='number',
                        step=1,
                        value=64,
                    ),
                ]
            ),
        ],
    ),
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
                'Путь к маскам',
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
                children='Запуск',
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


def return_dataset():
    return layout
