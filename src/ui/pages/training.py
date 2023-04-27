import dash_bootstrap_components as dbc
from dash import dcc, html
from dash_labs.plugins import register_page

from src.settings import Settings

# register_page(__name__)

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
            dbc.Input(
                id='model-type-input',
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
                id='learning-rate',
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
                id='epoch-cube_size',
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
                        'Размер батча',
                        className='mt-1',
                    ),
                    html.I(
                        className='fas fa-question-circle ml-1',
                        id='batch-cube-size-tip',
                        style={
                            'margin-left': '5px',
                        },
                    ),
                    dbc.Tooltip(
                        'Объем данных (количество строк/картинок), ' +
                        'подаваемый модели между вычислениями функции потерь',
                        target='batch-cube-size-tip',
                        className='pl-5',
                    ),
                ],
                className='text-muted',
            ),
            dbc.Input(
                id='batch-cube_size',
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
                id='device-type',
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
                value='..\\..\\data\\seistest1.npy',
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
                value='..\\..\\data\\faulttest1.npz',
            ),
        ],
        id='fault-mask-path',
    ),
    dbc.Form(
        [
            dbc.Label(
                'Путь к координатам масок',
                className='mt-1',
            ),
            dbc.Input(
                id='fault-mask-coords-input',
                style={
                    'width': '100%',
                },
                value='..\\..\\data\\masks_31_03_2023_23_40.txt',
            ),
        ],
        id='fault-mask-path',
    ),
    dbc.Form(
        [
            dbc.Button(
                id='training-submit-button',
                n_clicks=0,
                children='Запуск',
                color='secondary',
                size='sm',
                className='me-1 my-2',
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

layout = dbc.Card(
    [
        html.Div(id='div-training-placeholder'),
        dbc.Row(
            [
                tensorboard,
                dbc.Card(controls),
            ],
        ),
    ],
    style={'width': '100%'}
)


def return_training():
    return layout
