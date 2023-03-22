from typing import Optional

from plotly import express as px

from src.ui.read_segy import get_side_view, get_standart_view


def get_segy_path(
    data_store: Optional[dict] = None,
) -> str:
    """Get segy-path from dcc.Store."""
    if data_store is None:
        return ''
    return data_store.get('segy_path', '')


def get_slice(
    side_view: str,
    slice_id: int,
    segy_path: str,
):
    """Get slice from seg-y file."""
    if side_view == 'inline':
        segy_slice = get_side_view(
            segy_path,
            slice_id,
        )
    else:
        segy_slice = get_standart_view(
            segy_path,
            slice_id,
        )
    return px.imshow(segy_slice.T)


def get_slider_marks(max_value: int):
    """Update marks in sliders."""
    return {
        0: '0',
        (max_value // 4): str(max_value // 4),
        (max_value // 2): str(max_value // 2),
        (3 * max_value // 4): str(3 * max_value // 4),
        max_value: str(max_value),
    }
