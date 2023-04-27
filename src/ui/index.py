import dash_bootstrap_components as dbc
from dash import Input, Output, State, dash, dcc, html

# noinspection PyUnresolvedReferences
import src.ui.callbacks
from src.ui.app import _task, app
from src.ui.pages import return_slice_view, return_training, return_dataset

navbar = dbc.Navbar(
    children=[
        dbc.Button(
            "Sidebar",
            outline=True,
            color="secondary",
            className="mr-1 align-self-start",
            id="btn_sidebar"
        ),
    ],
    color="dark",
    dark=True,
    sticky="top",

)

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 62.5,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 0,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0.5rem 1rem",
    "background-color": "#f8f9fa",
}

SIDEBAR_HIDEN = {
    "position": "fixed",
    "top": 62.5,
    "left": "-16rem",
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0rem 0rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "transition": "margin-left .5s",
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE1 = {
    "transition": "margin-left .5s",
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

sidebar = dbc.Container(
    [
        html.H4("Fault segmentation"),
        html.Hr(),

        dbc.Nav(
            [
                dbc.NavLink(
                    "Просмотр срезов",
                    href="/slice-view",
                    id="page-1-link"
                ),
                dbc.NavLink(
                    "Настройка датасета",
                    href="/dataset",
                    id="page-2-link"
                ),
                dbc.NavLink(
                    "Обучение",
                    href="/training",
                    id="page-3-link"
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    id="sidebar",
    style=SIDEBAR_STYLE,
    # fluid=True
)

content = html.Div(
    [
        dash.page_container
    ],
    id="page-content",
    style={'background-color': '#ffffff'}
)

app.layout = html.Div(
    [
        dcc.Store(id='side_click'),
        dcc.Location(id="url"),
        dcc.Store(
            id='store',
            data={
                'segy_path': '..//..//data/F3_Dip.sgy',
                'segy-path-input': '..//..//data/F3_Dip.sgy',
            },
        ),
        navbar,
        sidebar,
        content,
    ],
)


@app.callback(
    [
        Output("sidebar", "style"),
        Output("page-content", "style"),
        Output("side_click", "data"),
    ],

    [Input("btn_sidebar", "n_clicks")],
    [
        State("side_click", "data"),
    ]
)
def toggle_sidebar(n, nclick):
    if n:
        if nclick == "SHOW":
            sidebar_style = SIDEBAR_HIDEN
            content_style = CONTENT_STYLE1
            cur_nclick = "HIDDEN"
        else:
            sidebar_style = SIDEBAR_STYLE
            content_style = CONTENT_STYLE
            cur_nclick = "SHOW"
    else:
        sidebar_style = SIDEBAR_STYLE
        content_style = CONTENT_STYLE
        cur_nclick = 'SHOW'

    return sidebar_style, content_style, cur_nclick


@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 4)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/page-{i}" for i in range(1, 4)]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return return_slice_view()
    elif pathname == "/slice-view":
        return return_slice_view()
    elif pathname == "/training":
        return return_training()
    elif pathname == "/dataset":
        return return_dataset()
    # If the user tries to reach a different page, return a 404 message
    return html.P(f"The pathname {pathname} was not recognised...")


if __name__ == '__main__':
    # path_seg = '..//..//data/Dutch Government_F3_entire_8bit seismic.segy'
    # print(get_segy_cube_shape(path_seg))
    # print(get_standart_view(path_seg, 1).shape)
    # print(get_side_view(path_seg, 1).shape)
    _task.launch()
    app.run_server(debug=True)
