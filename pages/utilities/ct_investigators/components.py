import dash_bootstrap_components as dbc
import dash_daq
import numpy as np
import pandas as pd
from dash import html, dcc, dash_table
import plotly.graph_objects as go

from pages.utilities.ct_const import *

filterCard = \
    dbc.Card(
        [
            dbc.CardBody(
                [
                    html.P("Category selection:"),
                    dcc.Dropdown(id="categorySelection",
                                 options=all_category,
                                 placeholder="Category...",
                                 multi=True),
                    html.Br(),
                    html.P("Sub-category selection:"),
                    dcc.Dropdown(id="subCategorySelection",
                                 options=all_sub_category,
                                 placeholder="Sub-category...",
                                 multi=True),
                    html.Br(),
                    html.P("Study type selection: "),
                    dcc.Dropdown(id="stypeSelection",
                                 options=all_stype,
                                 placeholder="Study types...",
                                 multi=True),
                    html.Br(),
                    html.P("Study status selection:"),
                    dcc.Dropdown(id="statusSelection",
                                 options=all_status,
                                 placeholder="Study status",
                                 multi=True),
                    html.Br(),
                    html.P("Study phases selection: "),
                    dcc.Dropdown(id="phasesSelection",
                                 options=['Unknow' if x is None else x for x in all_phases],
                                 placeholder="Study phases",
                                 multi=True),
                    # html.Br(),
                    # html.P("Sponsors class:"),
                    # dcc.Dropdown(id="sponsorsClass",
                    #              options=all_sponsors_class,
                    #              multi=True),

                    html.Br(),
                    html.Br(),
                    html.Plaintext("Filters return 15% of the total number of ct_studies", id="filtersInfos"),
                    html.Plaintext("Country selected : None", id="countryInfos")
                ]
            )
        ],
        class_name="card mb-4 border-1",
        style={"backgroundColor": "hsl(247.74, 52.54%, 98.43%)",
               "borderRadius": "15px"}
    )

mapSelection = \
    dbc.Card(
        [
            dbc.CardBody(
                [
                    dcc.Graph(id="investigators_map",
                              config={
                                  'displayModeBar': False,
                              }
                              ),
                ]
            )
        ],
        class_name="card mb-4 border-1",
        style={"backgroundColor": "hsl(247.74, 52.54%, 98.43%)",
               "borderRadius": "15px"}
    )

inv = investigators.copy()
count = inv[["name"]].copy()
count["studies_count"] = 1
count = count.groupby("name").count().reset_index().sort_values(by="studies_count", ascending=False)
count["repartition"] = round((count["studies_count"] / inv.shape[0]) * 100, 2)
count["repartition"] = count["repartition"].apply(lambda x: f"{x}%")

invDatatable = \
    dbc.Card(
        dbc.CardBody(
            [

                dash_table.DataTable(
                    id="invDataMapOutput",
                    data=count.to_dict('records'),
                    columns=[{"name": i, "id": i} for i in
                             count[["name", "studies_count", "repartition"]].columns],
                    page_size=15,
                    filter_action="native",
                    sort_action="native",
                    row_selectable="single",
                    style_cell={
                        'height': 'auto',
                        # all three widths are needed
                        'minWidth': '250px', 'width': '250px', 'maxWidth': '250px',
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
            ]
        ),
        style={"backgroundColor": "hsl(247.74, 52.54%, 98.43%)",
               "borderRadius": "15px",
               "marginTop": "15px"},
        class_name="card mb-4 border-1"
    )

investigatorsLocations = \
    dbc.Card(
        [
            dbc.CardBody(
                [

                ],
                id="invLocations"
            )
        ],
        style={"backgroundColor": "hsl(247.74, 52.54%, 98.43%)",
               "borderRadius": "15px",
               "marginTop": "15px",
               "height": "64vh"},
        class_name="card mb-4 border-1"
    )

investigatorInfos = \
    dbc.Card(
        [
            dbc.CardHeader("Select an investigator"),
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dcc.Markdown("**Name:** ", id="name",),
                                    dcc.Markdown("**City:** ", id="city"),
                                    dcc.Markdown("**State:** ", id="state"),
                                    dcc.Markdown("**Country:** ", id="country"),
                                    dcc.Markdown("**Continent:** ", id="continent")
                                ]
                            ),
                        ]
                    ),
                ]
            )
        ],
        style={"backgroundColor": "hsl(247.74, 52.54%, 98.43%)",
               "borderRadius": "15px",
               "marginTop": "15px"},
        class_name="card mb-4 border-1"
    )

studiesDatatable = \
    dash_table.DataTable(
        id="studiesDataInvOutput",
        data=s_base.drop(columns=["official_title", "investigators"], axis=1).to_dict('records'),
        columns=[{"name": i, "id": i} for i in
                 s_base.drop(columns=["official_title", "investigators"], axis=1).columns],
        page_size=10,
        filter_action="native",
        sort_action="native",
        style_cell={
            'height': 'auto',
            # all three widths are needed
            'minWidth': '180px', 'width': '180px', 'maxWidth': '200px',
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
