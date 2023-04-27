import dash_bootstrap_components as dbc
from dash import dcc, html


segy_settings = dbc.CardFooter(
    [
        dbc.Label('Выбор направления', className='pt-2'),
        dcc.Dropdown(
            [
                'xline',
                'inline',
            ],
            value='xline',
            id='perpendicular-way',
            style={'width': '50%'},
        ),
        dbc.Label('Путь к seg-y файлу', className='pt-2'),
        dbc.Input(
            id='segy-path-input',
            value='..//..//data/F3_Dip.sgy',
        ),
        dbc.Button(
            id='segy-path-submit-button',
            n_clicks=0,
            children='Загрузить',
            color='secondary',
            size='sm',
            className='me-1 my-2',
        ),
        html.Br(),
        dbc.Label('Путь к истинным маскам', className='pt-2'),
        dbc.Input(
            id='fault-mask-path-input',
            value='..//..//data/faulttest1.npz',
        ),
        dbc.Button(
            id='fault-mask-path-submit-button',
            n_clicks=0,
            children='Загрузить',
            color='secondary',
            size='sm',
            className='me-1 my-2',
        ),
        html.Br(),
        dbc.Label('Путь к предсказанным маскам', className='pt-2'),
        dbc.Input(
            id='predicted-mask-path-input',
            value='..//..//data/F3_Dip.sgy',
        ),
        dbc.Button(
            id='predicted-mask-path-submit-button',
            n_clicks=0,
            children='Загрузить',
            color='secondary',
            size='sm',
            className='me-1 my-2',
        ),
        html.Br(),
        dbc.Label('Прозрачность масок', className='pt-2'),
        dcc.Slider(
            value=100,
            step=1,
            min=0,
            max=100,
            marks={
                0: '0',
                25: '25',
                50: '50',
                75: '75',
                100: '100',
            },
            id='ask-alpha-channel-slider',
            tooltip={'placement': 'bottom'},
        ),
    ],
)


slice_view_row = dbc.Card(
    [
        dbc.CardHeader('Визуализация среза'),
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
        segy_settings
    ],
)


def return_slice_view():
    return slice_view_row
