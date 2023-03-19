"""
This example demonstrates sharing data between pages of a multi-page app.
Note that dcc.Store is in the app.py file so that it's accessible to all pages.
"""


from dash import html, dcc
import dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=external_stylesheets,
)

app.layout = html.Div(
    [
        html.H1("Multi Page App Demo: Sharing data between pages"),
        html.Div(
            [
                html.Div(
                    dcc.Link(f"{page['name']}", href=page["path"]),
                )
                for page in dash.page_registry.values()
            ]
        ),
        html.Div(
            [
                '../data/F3_Similarity.sgy',
                html.Br(),
                '../data/F3_Dip.sgy',
            ]
        ),
        html.Hr(),
        dcc.Store(
            id='intermediate-value',
            data={
                'segy_path': '../data/F3_Dip.sgy',
            },
        ),
        dash.page_container,
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True)
