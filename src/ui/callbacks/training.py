from dash import Input, Output, State, callback


@callback(
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
