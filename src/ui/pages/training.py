import dash_bootstrap_components as dbc
from dash import dcc, html
from dash_labs.plugins import register_page

import src.ui.callbacks.training  # noqa: WPS301 F401
from src.settings import Settings

register_page(__name__)

controls = [
    dbc.Form(
        [
            dbc.Label('Модель нейронной сети'),
            dcc.Dropdown(
                [
                    'Уже существующая',
                    'Новая',
                ],
                id='model-dropdown',
            ),
        ],
    ),
    dbc.Form(
        [
            html.Div(
                [
                    dbc.Label('Learning rate'),
                    html.I(
                        className='fas fa-question-circle',
                        id='learning-rate-tip',
                    ),
                    dbc.Tooltip(
                        'Коэффициент скорости обучения — это параметр ' +
                        'градиентных алгоритмов обучения нейронных сетей, ' +
                        'позволяющий управлять величиной коррекции весов на ' +
                        'каждой итерации. ',
                        target='learning-rate-tip',
                        className='pl-5',
                    ),
                ],
                className='text-muted',
            ),
            dbc.Input(
                id='learning-rate-value',
                type='number',
                step=Settings.LEARNING_RATE_STEP,
                value=Settings.BASE_LEARNING_RATE,
            ),
        ],
    ),
    dbc.Form(
        [
            dbc.Label('Количество эпох'),
            dbc.Input(
                id='epoch-value',
                type='number',
                step=1,
                value=10,
            ),
        ],
    ),
    dbc.Form(
        [
            html.Div(
                [
                    dbc.Label('Batch size'),
                    html.I(
                        className='fas fa-question-circle',
                        id='batch-size-tip',
                    ),
                    dbc.Tooltip(
                        'Объем данных (количество строк/картинок), ' +
                        'подаваемый модели между вычислениями функции потерь',
                        target='batch-size-tip',
                        className='pl-5',
                    ),
                ],
                className='text-muted',
            ),
            dbc.Input(
                id='batch-size-value',
                type='number',
                step=1,
                value=Settings.BASE_BATCH_SIZE,
            ),
        ],
    ),
]

tensorboard = html.Div(
    html.Iframe(
        src=f'http://localhost:{Settings.TENSORBOARD_PORT}/',
        style={
            'height': '100vh',
            'width': '100%',
        },
    ),
)

layout = dbc.Container(
    [
        dbc.Button(
            children='Настройки',
            id='collapse-model-settings-btn',
        ),
        dbc.Row(
            [
                dbc.Collapse(
                    dbc.Card(controls, body=True),
                    id='collapse-model-settings',
                    is_open=True,
                    class_name='col-md-3',
                    dimension='width',
                ),
                dbc.Col(
                    tensorboard,
                ),
            ],
        ),
    ],
)
