import datetime

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, dash_table, html, dcc
from dateutil.relativedelta import relativedelta

from pages.utilities.studies.components import *


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
                dbc.Col([newStudiesTitle, newStudiesDatatable], width="auto"),
            ]
        )
    ]
),


@callback(Output("newStudiesDatatable", "data"),
          Input("newStudiesDate", "value"))
def UpdateNewStudiesDatatable(selection):
    df = s_base.copy()
    now = datetime.now().strftime("%Y-%m-%d")
    now = datetime.strptime(now, "%Y-%m-%d")

    if selection == "day":
        pass
    elif selection == "week":
        pass
    elif selection == "month":
        pass
    elif selection == "year":
        pass

    return df.to_dict('records')
