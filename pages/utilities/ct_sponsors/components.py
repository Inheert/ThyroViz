from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import math
from pages.utilities.ct_helpers import *

funnel = \
    dbc.CardGroup(
        [
            dbc.Card(
                [
                    dbc.CardHeader(children="Sponsors filters",
                                   style={"textAlign": "center",
                                          "fontSize": "15px"}),
                    dbc.CardBody(
                        [
                            dcc.Dropdown(id="sponsors_class",
                                         options=all_sponsors_class,
                                         value=[],
                                         placeholder="Select sponsors class...",
                                         multi=True),
                            html.Br(),
                            dcc.Dropdown(id="studies_category",
                                         options=all_category,
                                         value=[],
                                         placeholder="Select category...",
                                         multi=True),
                            html.Br(),
                            dcc.Dropdown(id="studies_sub_category",
                                         options=all_sub_category,
                                         value=[],
                                         placeholder="Select sub-category...",
                                         multi=True),
                            html.Br(),
                            dcc.Dropdown(id="studies_type",
                                         options=all_stype,
                                         value=[],
                                         placeholder="Select studies type...",
                                         multi=True),
                            html.Br(),
                            dcc.Dropdown(id="studies_status",
                                         options=all_status,
                                         placeholder="Select studies status...",
                                         value=[],
                                         multi=True),
                            html.Br(),
                            dcc.Dropdown(id="studies_phases",
                                         options=all_phases,
                                         value=[],
                                         placeholder="Select studies phases...",
                                         multi=True),
                            html.Hr(),
                            dbc.Row(
                                [
                                    dbc.Col(html.P(children="Sort by:"),
                                            width="auto"),
                                    dbc.Col(
                                        dcc.Dropdown(id="sort_by",
                                                     options={"asc": "A -> Z",
                                                              "desc": "Z -> A",
                                                              "most": "Most amount of studies",
                                                              "least": "Least amount of studies"},
                                                     value="asc")
                                    )
                                ],
                                align="end"
                            ),
                            html.Br(),
                            html.Br(),
                        ],
                    ),
                ],
                style={
                    "maxWidth": "12vw",
                    "width": "12vw"
                }
            ),
            dbc.Card(
                [
                    dbc.CardHeader("Sponsors list",
                                   style={"textAlign": "center",
                                          "fontSize": "15px"}
                                   ),

                    dbc.CardBody(
                        children=[
                            dbc.Row(id="sponsors_list"),
                            dbc.Row(
                                dbc.Col(
                                    dbc.Pagination(id="sponsors_pagination",
                                                   max_value=5,
                                                   fully_expanded=False),
                                    style={"display": "flex",
                                           "justifyContent": "center",
                                           "marginTop": "2vh"}
                                ),
                            )
                        ]
                    ),
                ],
                style={
                    "maxWidth": "25vw",
                    "width": "25vw",
                    'height': "75vh",
                    "maxHeight": "75vh"
                }
            ),
            dbc.Card(
                [
                    dbc.CardHeader("Sponsors Informations", style={"textAlign": "center"}),
                    dbc.CardBody(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dcc.Markdown(children="__Name:__", id="sponsors_name"),
                                        ]
                                    ),
                                    dbc.Col(
                                        [
                                            dcc.Markdown(children="__Class:__", id="sponsors_class")
                                        ]
                                    ),
                                    dbc.Col(
                                        [
                                            dcc.Markdown(children="__Number of studies:__", id="sponsors_studies_count")
                                        ]
                                    )
                                ],
                                align="center"
                            )
                        ]
                    )
                ]
            )
        ]
    )

sponsorsClassPieChart = \
    dbc.Card(
        dbc.CardBody(
            [
                dcc.Graph(id="sponsorsClassPie", config={"displayModeBar": False},
                          style={"width": "25vw"})
            ]
        ),
        class_name="card mb-4 border-1",
        style={"backgroundColor": "hsl(247.74, 52.54%, 98.43%)",
               "borderRadius": "15px",
               }
    )

filters = \
    dbc.Card(
        dbc.CardBody(
            [
                html.Plaintext("Sponsors class:"),
                dcc.Dropdown(
                    options=all_sponsors_class,
                    id="sp_class"
                ),
                html.Br(),

                html.Plaintext("Studies category:"),
                dcc.Dropdown(
                    options=all_category,
                    id="s_category"
                ),
                html.Br(),

                html.Plaintext("Studies sub-category:"),
                dcc.Dropdown(
                    options=all_sub_category,
                    id="s_sub_category"
                ),
                html.Br(),

                html.Plaintext("Studies type:"),
                dcc.Dropdown(
                    options=all_stype,
                    id="s_study_type"
                ),
                html.Br(),

                html.Plaintext("Studies phases:"),
                dcc.Dropdown(
                    options=all_phases,
                    id="s_study_phases"
                ),
                html.Br(),

                html.Plaintext("Studies status:"),
                dcc.Dropdown(
                    options=all_status,
                    id="s_study_status"
                ),
                html.Br(),

                html.Plaintext("Time perspective:"),
                dcc.Dropdown(
                    options=all_time_perspective,
                    id="study_time_perspective"
                ),
                html.Br(),

                html.Plaintext("Intervention model:"),
                dcc.Dropdown(
                    options=all_int_models,
                    id="study_int_model"
                ),
                html.Br(),

                html.Plaintext("Observational model:"),
                dcc.Dropdown(
                    options=all_obs_models,
                    id="study_obs_model"
                ),
                html.Br(),
            ]
        ),
        style={
            "borderRadius": "15px"
        }
    )

sponsorsDatatable = \
    dash_table.DataTable(
        id="sponsorsDatatable",
        data=sponsors.to_dict('records'),
        columns=[{"name": i, "id": i} for i in
                 sponsors[["name", 'new_class']].columns],
        page_size=10,
        filter_action="native",
        sort_action="native",
        row_selectable="single",
        style_cell={
            'height': 'auto',
            # all three widths are needed
            'minWidth': '200px', 'width': '200px', 'maxWidth': '200px',
            'whiteSpace': 'normal'
        },
        style_header={
            'backgroundColor': "#0D6986",
            "color": "white",
            "fontWeight": 900,
            "fontSize": "12px"
        },
        style_table={
            'borderRadius': '15px',
            'overflow': 'hidden',
            'overflowX': 'auto'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(223, 226, 232)',
                'color': 'black'
            },
            {
                'if': {'row_index': 'even'},
                'backgroundColor': 'rgb(245, 249, 255)'
            }
        ]
    )
