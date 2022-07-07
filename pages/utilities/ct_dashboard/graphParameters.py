import dash_bootstrap_components as dbc
from dash import html, dcc
from pages.utilities.ct_const import s_base
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
                               id="CRP_reset",
                               style={
                                   'maxHeight': "2vmax"
                               }),
                    width="auto"
                )
            ],
            align="center"
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
                "maxWidth": "300px",
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
                "maxWidth": "300px",
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
        dcc.Checklist(
            id="CRP_highlight",
            options=["Highlight"],
            inputStyle={
                "marginRight": "6px"
            }
        )
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
                               id="SDO_reset",
                               style={
                                   'maxHeight': "2vmax"
                               }
                               ),
                    width="auto"
                )
            ],
            align="center"
        ),
        html.Hr(),
        html.Plaintext("Figure type:",
                       style={
                           "marginBottom": "-2px"
                       }),
        dcc.RadioItems(
            id="SDO_radioItems",
            options=["Line", "Bar"],
            value="Line",
            inputStyle={
                "marginRight": "6px"
            }
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
        html.Br(),
        dcc.Checklist(
            id="SDO_highlight",
            options=["Highlight"],
            inputStyle={
                "marginRight": "6px"
            }
        )
    ]

parametersItem3 = \
    [
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    html.H5("Studies repartition")
                ),
                dbc.Col(
                    dbc.Button("Reset",
                               id="SR_reset",
                               style={
                                   'maxHeight': "2vmax"
                               }
                               ),
                    width="auto"
                )
            ],
            align="center"
        ),
        html.Hr(),
        html.Plaintext("Repartition source:",
                       style={
                           "marginBottom": "0px"
                       }
                       ),
        dcc.Dropdown(
            id="SR_dropdown",
            options=[
                {'label': 'Intervention model', 'value': 'intervention_model'},
                {'label': 'Observational model', 'value': 'observational_model'},
                {'label': 'Overall status', 'value': 'overall_status'},
                {'label': 'Study phases', 'value': 'study_phases'},
                {'label': 'Study type', 'value': 'study_type'},
                {'label': 'Time perspective', 'value': 'time_perspective'},
            ],
            value="study_phases",
        ),
        html.Br(),
        html.Plaintext("View the repartition source by:",
                       style={
                           "marginBottom": "0px"
                       }
                       ),
        dcc.RadioItems(
            id="SR_radioItems",
            options=[
                {'label': 'all studies', 'value': 'all'},
                {'label': 'the selected source', 'value': 'only'}
            ],
            value='all',
            inputStyle={
                "marginRight": "6px"
            }
        ),
        html.Br(),
        dcc.Checklist(
            id="SR_highlight",
            options=["Highlight"],
            inputStyle={
                "marginRight": "6px"
            }
        )
    ]
