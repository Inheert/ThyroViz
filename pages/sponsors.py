import dash
from dash import Input, Output, State, callback, dash_table, html, dcc
import dash_bootstrap_components as dbc
from pages.utilities.sponsors.components import *
from pages.utilities.sponsors.callbacks import *

dash.register_page(__name__)

layout = html.Div([
    dbc.Row(
        html.H1("Sponsors", style={"textAlign": "center"})
    ),
    dbc.Row([
        dbc.Col([
            sponsorsClassPieChart
        ],
            width="auto",
            style={
                "display": "flex",
                "alignItems": "top",
                "justifyContent": "left",
                "horizontalAlign": "center",
            },
        ),
        dbc.Col([filters],
                width=2),
        dbc.Col(sponsorsDatatable)
    ])
]),
