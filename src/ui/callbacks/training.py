from dash import Input, Output, State, callback
from dash.exceptions import PreventUpdate
from src.ui.app import _task, app


@app.callback(
    Output('collapse-model-settings', 'is_open'),
    [Input('collapse-model-settings-btn', 'n_clicks')],
    [State('collapse-model-settings', 'is_open')],
    prevent_initial_call=True,
)
def collapse_training_settings(n_clicks, is_open):
    """Collapse seg-y settings block."""
    if n_clicks:
        return not is_open
    return is_open


@app.callback(
    Output('div-training-placeholder', 'children'),
    Input('training-submit-button', 'n_clicks'),
    State('model-type-dropdown', 'value'),
    State('model-type-input', 'value'),
    State('learning-rate', 'value'),
    State('epoch-cube_size', 'value'),
    State('batch-cube_size', 'value'),
    State('device-type', 'value'),
    State('segy-input', 'value'),
    State('fault-mask-input', 'value'),
    State('fault-mask-coords-input', 'value'),
    prevent_initial_call=True,
)
def start_training(
    n_clicks,
    model_type: str,
    model_path: str,
    lr_value: float,
    epoch_size: int,
    batch_size: int,
    device_type: str,
    seis_path: str,
    fault_mask_path: str,
    coords_mask_path: str,
):
    if not n_clicks:
        raise PreventUpdate()
    print('Start training')
    _task.train(
        model_type,
        model_path,
        lr_value,
        epoch_size,
        batch_size,
        device_type,
        seis_path,
        fault_mask_path,
        coords_mask_path,
    )