import plotly.express as px
import segyio
from dash import Input, Output, State, callback, dcc, html, register_page

from src.read_segy import get_segy_cube_shape

register_page(
    __name__,
    top_nav=True,
)

segy_path = '../data/F3_Dip.sgy'

xline_max, iline_max = get_segy_cube_shape(segy_path)[:2]
layout = html.Div(
    id='main-layout',
    children=[
        dcc.Slider(
            min=0,
            max=iline_max,
            step=1,
            value=0,
            id='slice-slider',
            marks={
                0: '0',
                (iline_max // 4): str(iline_max // 4),
                (iline_max // 2): str(iline_max // 2),
                (3 * iline_max // 4): str(3 * iline_max // 4),
                iline_max: str(iline_max),
            }
        ),
        html.Div(
            id='div-example-graph',
        ),
        dcc.Input(
            id='segy-path-input',
            value='../data/F3_Dip.sgy',
        ),
        html.Button(
            id='segy-path-submit-button',
            n_clicks=0,
            children='Submit',
        ),
        html.Div(id='my-output'),
    ]
)



@callback(
    Output('div-example-graph', 'children'),
    Input('slice-slider', 'value')
)
def _get_standart_view(
    iline_id: int = 1,
) -> object:
    try:
        with segyio.open(segy_path) as segyfile:
            xlines_count = len(segyfile.xlines)
            segy_slice = segyfile.trace.raw[iline_id::xlines_count]
            fig = px.imshow(segy_slice.T)
    except FileNotFoundError:
        return html.Div(
            [
                'Файл не найден. Проверьте правильность пути к файлу.'
            ]
        )
    return dcc.Graph(
        id='example-graph',
        figure=fig,
    )


@callback(
    Output('slice-slider', 'max'),
    Input('segy-path-submit-button', 'n_clicks'),
    State('segy-path-input', 'value'),
)
def update_slider_iline_max(n_clicks, _segy_path):
    global segy_path
    segy_path = _segy_path
    if _segy_path is None:
        segy_path = '../data/F3_Dip.sgy'
    _, new_iline_max = get_segy_cube_shape(segy_path)[:2]
    return new_iline_max


@callback(
    [Output('slice-slider', 'marks'),
     Output('slice-slider', 'value'),
     ],
    Input('segy-path-submit-button', 'n_clicks'),
    State('segy-path-input', 'value'),
)
def update_slider_marks(n_clicks, _segy_path):
    global segy_path
    segy_path = _segy_path
    if _segy_path is None:
        segy_path = '../data/F3_Dip.sgy'
    _, new_iline_max = get_segy_cube_shape(segy_path)[:2]
    return {
        0: '0',
        (new_iline_max // 4): str(new_iline_max // 4),
        (new_iline_max // 2): str(new_iline_max // 2),
        (3 * new_iline_max // 4): str(3 * new_iline_max // 4),
        new_iline_max: str(new_iline_max),
    }, 0


@callback(
    Output('intermediate-value', 'data'),
    Input('segy-path-submit-button', 'n_clicks'),
    State('segy-path-input', 'value'),
)
def save_segy_path(n_clicks, _segy_path):
    return {'segy_path': _segy_path}
