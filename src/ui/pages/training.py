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
                value='Новая',
                id='model-type-dropdown',
            ),
        ],
    ),
    dbc.Form(
        [
            dbc.Label(
                'Путь к весам модели',
                className='mt-1',
            ),
            dcc.Input(
                id='model-type-dropdown',
                style={
                    'width': '100%',
                },
            ),
        ],
        id='model-weights-path',
    ),
    dbc.Form(
        [
            html.Div(
                [
                    dbc.Label(
                        'Learning rate',
                        className='mt-1',
                    ),
                    html.I(
                        className='fas fa-question-circle',
                        id='learning-rate-tip',
                        style={
                            'margin-left': '5px',
                        },
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
            dbc.Label(
                'Количество эпох',
                className='mt-1',
            ),
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
                    dbc.Label(
                        'Batch size',
                        className='mt-1',
                    ),
                    html.I(
                        className='fas fa-question-circle ml-1',
                        id='batch-size-tip',
                        style={
                            'margin-left': '5px',
                        },
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
    dbc.Form(
        [
            html.Div(
                [
                    dbc.Label(
                        'Вид девайса',
                        className='mt-1',
                    ),
                    html.I(
                        className='fas fa-question-circle ml-1',
                        id='device-type-tip',
                        style={
                            'margin-left': '5px',
                        },
                    ),
                    dbc.Tooltip(
                        'На каком устройстве будет обучаться модель, ' +
                        'в случае видеокарты, требуется Nvidia любого ' +
                        'поколения. Видеокарта в десятки раз быстрее ' +
                        'проводит обучение.',
                        target='device-type-tip',
                        className='pl-5',
                    ),
                ],
                className='text-muted',
            ),
            dcc.Dropdown(
                [
                    'Процессор',
                    'Видеокарта',
                ],
                value='xline',
                id='device-type-value',
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
