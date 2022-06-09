import datetime
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, dash_table, html, dcc
from dateutil.relativedelta import relativedelta

from pages.utilities.studies.components import *
from pages.utilities.studies.callbacks import *

dash.register_page(__name__)

layout = html.Div(
    [
        dbc.Row(
            [
                html.H1("Studies overview", style={'textAlign': 'center'})
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col([newStudiesTitle, newStudiesDatatable, newStudiesModal], width="auto"),
                dbc.Col(),
                dbc.Col([completedStudiesTitle, completedStudiesDatatable, completedStudiesModal], width='auto')
            ]
        ),
        html.Br(),
        html.Hr(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col([allStudiesHeader, allStudiesModal]),
            ]
        ),
        html.Br(),
        dbc.Row(
          [
              dbc.Col(allStudiesDatatable)
          ]
        )
    ]
),
