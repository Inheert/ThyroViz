import dash_bootstrap_components as dbc
from dash import html, dcc
from pages.utilities.const import s_base
import dash_daq as daq
from datetime import datetime

parametersItem1 = \
    [
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    html.H5("Category repartition")
                ),
                dbc.Col(
                    dbc.Button("Reset",
                               id="CRP_reset"),
                    width="auto"
                )
            ]
        ),
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
                "maxWidth": "300px"
            }),
        html.Plaintext("Studies age selection:",
                       style={
                           "marginBottom": "-2px"
                       }),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Plaintext("Min:"),
                        daq.NumericInput(
                            id="CRP_minAge",
                            min=0,
                            max=100,
                            value=0
                        )
                    ],
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "left",
                        "horizontalAlign": "center",
                    }
                ),
                dbc.Col(
                    [
                        html.Plaintext("Max:"),
                        daq.NumericInput(
                            id="CRP_maxAge",
                            min=0,
                            max=100,
                            value=100
                        )
                    ],
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "left",
                        "horizontalAlign": "center",
                    }
                )
            ]
        ),
        html.Br(),
    ]

parametersItem2 = \
    [
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    html.H5("Studies date overview")
                ),
                dbc.Col(
                    dbc.Button("Reset",
                               id="SDO_reset"),
                    width="auto"
                )
            ]
        ),
        html.Hr(),
        html.Plaintext("Figure type:",
                       style={
                           "marginBottom": "-2px"
                       }),
        dcc.RadioItems(
            id="SDO_radioItems",
            options=["Line", "Bar"],
            value="Line"
        ),
        html.Plaintext("Columns displaying:",
                       style={
                           "marginBottom": "0px"
                       }),
        dcc.Checklist(
            id="SDO_checklist",
            options=[
                {'label': 'Show first submitted date', 'value': 'study_first_submitted_date'},
                {'label': 'Show first primary completion date', 'value': 'primary_completion_date'},
                {'label': 'Show completion date', 'value': 'completion_date'}
            ],
            value=["study_first_submitted_date"],
            inputStyle={
                "marginRight": "6px"
            }
        ),
        html.Plaintext("Display by month:",
                       style={
                           "marginBottom": "0px"
                       }),
        dcc.Checklist(
            id="SDO_monthDisplay",
            options=[
                {'label': 'Display by month', 'value': 'month'},
            ],
            value=[],
            inputStyle={
                "marginRight": "6px"
            }
        ),
        html.Plaintext("Year range selection:",
                       style={
                           "marginBottom": "-2px"
                       }),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Plaintext("Min:"),
                        daq.NumericInput(
                            id="SDO_minYear",
                            min=1950,
                            max=2150,
                            value=1999,
                            size=65
                        )
                    ],
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "left",
                        "horizontalAlign": "center",
                    }
                ),
                dbc.Col(
                    [
                        html.Plaintext("Max:"),
                        daq.NumericInput(
                            id="SDO_maxYear",
                            min=1999,
                            max=2150,
                            value=datetime.now().year,
                            size=65
                        )
                    ],
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "left",
                        "horizontalAlign": "center",
                    }
                )
            ]
        ),
    ]

studiesDateOverviewParameters = \
    [
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    html.H5("Studies date overview")
                ),
                dbc.Col(
                    dbc.Button("Reset",
                               id="SDO_reset"),
                    width="auto"
                )
            ]
        ),
        html.Hr(),
        html.Plaintext("Figure type:",
                       style={
                           "marginBottom": "-2px"
                       }),
        dcc.RadioItems(
            id="SDO_radioItems",
            options=["Line", "Bar"],
            value="Line"
        ),
        html.Plaintext("Columns displaying:",
                       style={
                           "marginBottom": "0px"
                       }),
        dcc.Checklist(
            id="SDO_checklist",
            options=[
                {'label': 'Show first submitted date', 'value': 'study_first_submitted_date'},
                {'label': 'Show first primary completion date', 'value': 'primary_completion_date'},
                {'label': 'Show completion date', 'value': 'completion_date'}
            ],
            value=["study_first_submitted_date"],
            inputStyle={
                "marginRight": "6px"
            }
        ),
        html.Plaintext("Display by month:",
                       style={
                           "marginBottom": "0px"
                       }),
        dcc.Checklist(
            id="SDO_monthDisplay",
            options=[
                {'label': 'Display by month', 'value': 'month'},
            ],
            value=[],
            inputStyle={
                "marginRight": "6px"
            }
        ),
        html.Plaintext("Year range selection:",
                       style={
                           "marginBottom": "-2px"
                       }),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Plaintext("Min:"),
                        daq.NumericInput(
                            id="SDO_minYear",
                            min=1950,
                            max=2150,
                            value=1999,
                            size=65
                        )
                    ],
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "left",
                        "horizontalAlign": "center",
                    }
                ),
                dbc.Col(
                    [
                        html.Plaintext("Max:"),
                        daq.NumericInput(
                            id="SDO_maxYear",
                            min=1999,
                            max=2150,
                            value=datetime.now().year,
                            size=65
                        )
                    ],
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "left",
                        "horizontalAlign": "center",
                    }
                )
            ]
        ),
    ]

CRP_default = \
    [
        dcc.Store(id="CRP_studiesType"),
        dcc.Store(id="CRP_studiesStatus"),
        dcc.Store(id="CRP_minAge"),
        dcc.Store(id="CRP_maxAge"),
        dcc.Store(id="CRP_reset"),
    ]

SDO_default = \
    [
        dcc.Store(id="SDO_reset"),
        dcc.Store(id="SDO_radioItems"),
        dcc.Store(id="SDO_minYear"),
        dcc.Store(id="SDO_maxYear"),
        dcc.Store(id="SDO_checklist"),
        dcc.Store(id="SDO_monthDisplay")
    ]
