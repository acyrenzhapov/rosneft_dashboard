from dash import Input, Output, State, callback
from dash.exceptions import PreventUpdate
from src.network.data_preparation import DataPreparation


@callback(
    Output('div-placeholder', 'children'),
    Input('dataset-submit-button', 'n_clicks'),
    State('dataset-cube_size', 'value'),
    State('segy-input', 'value'),
    State('fault-mask-input', 'value'),
    prevent_initial_call=True,
)
def create_dataset(
    n_clicks,
    dataset_size: int,
    seis_path: str,
    fault_mask_path: str,
):
    if not n_clicks:
        raise PreventUpdate()
    dp = DataPreparation(
        fault_mask_path,
        dataset_size,
        64,
        dataset_type='train',
        threshold_percent=0.1
    )
    dp.create_dataset()
