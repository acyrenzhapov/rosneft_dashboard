from typing import Optional

from dash import Input, Output, State, callback
from dash.development.base_component import Component
from plotly.express import imshow

from src.ui.read_segy import get_segy_cube_shape
from src.ui.utils import get_segy_path, get_slice, get_slider_marks


@callback(
    Output('div-example-graph', 'figure'),
    Input('slice-slider', 'value'),
    Input('perpendicular-way', 'value'),
    Input('store', 'data'),
)
def _get_slice_view(
    slice_id: int = 1,
    side_view: str = 'inline',
    data_store: Optional[dict] = None,
) -> Component:
    """Return component with seg-y slice."""
    segy_path = get_segy_path(data_store)
    fig = imshow(
        [[1]],
    )
    try:
        fig = get_slice(
            side_view,
            slice_id,
            segy_path,
        )
    except FileNotFoundError:
        return fig
    return fig


@callback(
    Output('slice-slider', 'max'),
    Input('segy-path-submit-button', 'n_clicks'),
    Input('perpendicular-way', 'value'),
    Input('store', 'data'),
    State('segy-path-input', 'value'),
)
def update_slider_inline_max(
    n_clicks: int = 0,
    side_view: str = 'inline',
    data_store: Optional[dict] = None,
    _segy_path: str = '',
):
    """Update max value in slider."""
    segy_path = get_segy_path(data_store)
    new_xline_max, new_inline_max = get_segy_cube_shape(segy_path)[:2]
    if side_view == 'xline':
        return new_inline_max
    return new_xline_max


@callback(
    Output('slice-slider', 'marks'),
    Input('segy-path-submit-button', 'n_clicks'),
    Input('store', 'data'),
    Input('perpendicular-way', 'value'),
    State('segy-path-input', 'value'),
)
def update_slider_marks(
    n_clicks: int = 0,
    data_store: Optional[dict] = None,
    side_view: str = 'inline',
    _segy_path: str = '',
):
    """Update slider marks in ui."""
    segy_path = get_segy_path(data_store)
    new_xline_max, new_inline_max = get_segy_cube_shape(segy_path)[:2]
    if side_view == 'xline':
        return get_slider_marks(new_inline_max)
    return get_slider_marks(new_xline_max)


@callback(
    Output('store', 'data'),
    Input('segy-path-submit-button', 'n_clicks'),
    State('segy-path-input', 'value'),
)
def save_segy_path(
    n_clicks: int,
    _segy_path: str,
):
    """Update store."""
    return {'segy_path': _segy_path}
