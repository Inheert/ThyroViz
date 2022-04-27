import dash_bootstrap_components as dbc
from dash import html, dcc
from pages.utilities.const import s_base

categoryRepartitionPie = \
    [
        html.H5("Category repartition"),
        html.Hr(),
        html.Plaintext("Studies type:",
                       style={
                           "marginBottom": "-2px"
                       }),
        dcc.Dropdown(
            id="CRP_studiesType",
            options=s_base.study_type.unique(),
            value=[],
            multi=True,
            style={
                "maxWidth": "300px"
            }),

        html.Plaintext("Studies status:",
                       style={
                           "marginBottom": "-2px"
                       }),
        dcc.Dropdown(
            id="CRP_studiesStatus",
            options=s_base.overall_status.unique(),
            value=[],
            multi=True,
            style={
                "maxWidth": "500px"
            }),
        html.Hr(),
    ]

default = \
    [
        dcc.Store(id="CRP_studiesType"),
        dcc.Store(id="CRP_studiesStatus")
    ]
