import dash
import dash_bootstrap_components as dbc
import dash_labs as dl
from src.ui.tasks.segmentation_task import SegmentationTask

FONT_AWESOME = 'https://use.fontawesome.com/releases/v5.10.2/css/all.css'

app = dash.Dash(
    __name__,
    plugins=[dl.plugins.pages],
    suppress_callback_exceptions=True,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        FONT_AWESOME,
    ],
)
app.config.suppress_callback_exceptions = True

app.title = 'Fault segmentation'

_task = SegmentationTask()
