import dash_daq
import numpy as np
from dash import dash_table
from geopy.geocoders import Nominatim

from pages.utilities.helpers import *
from pages.utilities.dashboard.graphParameters import *

topCardNav1 = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink(
            children=dbc.CardGroup(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H1(f"{len(studies['nct_id'].unique())}",
                                        className="card-title"),
                                html.P("studies in progress", className="card-text"),
                            ],
                        ),
                    ),
                    dbc.Card(
                        html.Div(className="bi bi-eye", style=card_icon),
                        color="#247cfd",
                        style={"maxWidth": "4vw"},
                    ),
                ],
                className="mt-4 shadow",
            ),
            active="exact",
            href="/studies"
        ),
        )
    ],
    vertical=False,
    fill=True
)

topCardNav2 = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink(
            children=
            dbc.CardGroup(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H1(
                                    f"{s_base[(s_base['study_first_submitted_date'] >= f'{datetime.now().year}-{datetime.now().month - 1}') & (s_base['study_first_submitted_date'] < f'{datetime.now().year}-{datetime.now().month}')].shape[0]}",
                                    className="card-title"),
                                html.P("new studies this month", className="card-text", ),
                            ]
                        )
                    ),
                    dbc.Card(
                        html.Div(className="bi bi-clipboard2-plus", style=card_icon),
                        color="#0D6EFD",
                        style={"maxWidth": "4vw"},
                    ),
                ],
                className="mt-4 shadow",
            ),
            active="exact",
            href="/studies"
        ),
        )
    ],
    vertical=False,
    fill=True
)

topCardNav3 = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink(
            children=
            dbc.CardGroup(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H1(
                                    f"{len(sponsors.name.unique())}",
                                    className="card-title"),
                                html.P("Number of sponsors",
                                       className="card-text"),
                            ]
                        )
                    ),
                    dbc.Card(
                        html.Div(className="bi bi-people", style=card_icon),
                        color="#024ebf",
                        style={"maxWidth": "4vw"},
                    ),
                ],
                className="mt-4 shadow",
            ),
            active="exact",
            href="/sponsors"
        ),
        )
    ],
    vertical=False,
    fill=True
)

topCardNav4 = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink(
            children=
            dbc.CardGroup(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H1(
                                    f"{len(investigators.name.unique())}",
                                    className="card-title"),
                                html.P("Number of investigators",
                                       className="card-text", ),
                            ]
                        )
                    ),
                    dbc.Card(
                        html.Div(className="bi bi-clipboard2-plus", style=card_icon),
                        color="#013684",
                        style={"maxWidth": "4vw"},
                    ),
                ],
                className="mt-4 shadow",
            ),
            active="exact",
            href="/investigators"
        ),
        )
    ],
    vertical=False,
    fill=True
)

lightStatistic1 = \
    html.Div(
        [
            dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                html.P("Number of new studies by year"),
                                html.Hr()
                            ],
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Div(id="card1Output1",),
                                    width="auto",
                                    style={
                                        "display": "flex",
                                        "alignItems": "center",
                                        "justifyContent": "left",
                                    }
                                ),
                                dbc.Col(
                                    html.Div(id="card1Output2"),
                                    width="auto",
                                ),
                                dbc.Col(
                                    html.Div(id="card1Output3"),
                                    width="auto",
                                )
                            ],
                            align="end"
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dash_daq.NumericInput(
                                        id="card1Input1",
                                        value=2022,
                                        min=1999,
                                        max=datetime.now().year,
                                        size=65
                                    ),
                                    width="auto",
                                    style={
                                    }
                                ),
                                dbc.Col(
                                    html.P("to: ",
                                           style={
                                               "verticalAlign": "bottom",
                                               "alignItems": "end"
                                           }),
                                    width="auto",
                                    style={
                                        "marginLeft": "-10px",
                                        "marginRight": "-10px",
                                        "display": "flex",
                                        "alignItems": "end",
                                        "justifyContent": "left",
                                    }
                                ),
                                dbc.Col(
                                    dash_daq.NumericInput(
                                        id="card1Input2",
                                        value=2021,
                                        min=1999,
                                        max=datetime.now().year,
                                        size=65
                                    ),
                                    width="auto",
                                ),
                            ]
                        ),
                    ]
                ),
                class_name="card mb-4 border-1",
                style={"backgroundColor": "#fdfdfd",
                       "borderRadius": "15px"}
            ),
        ]
    )

lightStatistic2 = \
    html.Div(
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            html.P("Studies repartition by sponsors class"),
                            html.Hr()
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    id="card2Output1",
                                ),
                                width="auto",
                                style={
                                    "display": "flex",
                                    "alignItems": "center",
                                    "justifyContent": "left",
                                }
                            ),
                            dbc.Col(
                                html.H3('-- %',
                                        id="card2Output2",
                                        ),
                                width="auto",
                            ),
                            dbc.Col(
                                html.Plaintext('--',
                                               id="card2Output3"),
                                width="auto",
                            )
                        ],
                        align="end"
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.P("Sponsors class:",
                                           style={
                                               "verticalAlign": "bottom",
                                               "alignItems": "end"
                                           }
                                           )
                                ],
                                width="auto",
                                style={
                                    "display": "flex",
                                    "alignItems": "end",
                                    "justifyContent": "left",
                                }
                            ),
                            dbc.Col(
                                [
                                    dcc.Dropdown(
                                        id="card2Input1",
                                        options=[x for x in sponsors.new_class.unique()],
                                        value="Industry"
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),
            class_name="card mb-4 border-1",
            style={"backgroundColor": "#fdfdfd",
                   "borderRadius": "15px"}
        )
    )

category = GetCategoryPercent(groupby="category", sortby=["nct_id"], drop_duplicates=["category", "nct_id"])
leftCategoryCard = \
    dcc.Tabs(id="leftSideTab",
             value="tab1",
             style={
                 'maxHeight': '5vmax',
                 'maxWidth': "20vmax"
             },
             children=[
                 dcc.Tab(label="Category",
                         value="tab1",
                         id="leftTab1",
                         style=tab_style,
                         selected_style=tab_selected_style,
                         children=[
                             dbc.Card(
                                 dbc.CardBody(
                                     [
                                         html.H6(f"{category.loc[x]['category']}",
                                                 className="card-title",
                                                 id=f"title-{category.loc[x]['category']}"),
                                         html.P(
                                             f"{category.loc[x]['nct_id']}%"
                                         ),
                                         dbc.Button(children="Select",
                                                    id=f"button-{category.loc[x]['category']}",
                                                    style={
                                                        'fontSize': '0.5vmax',
                                                        'maxHeight': '2vmax'
                                                    },
                                                    color="primary",
                                                    outline=True)
                                     ],
                                 ),
                                 className="mb-1 shadow-sm",
                                 style={
                                     "backgroundColor": "rgba(0,0,0,0)",
                                     "maxWidth": "20vmax",
                                 }
                             ) for x in category.index
                         ],
                         ),

                 dcc.Tab(label="Parameters",
                         value="tab2",
                         id="leftTab2",
                         style=tab_style,
                         selected_style=tab_selected_style,
                         children=[
                             dbc.Accordion(
                                 always_open=True,
                                 children=[
                                     dbc.AccordionItem(
                                         title="Category/Sub-category repartition",
                                         id="parametersItem1",
                                         children=parametersItem1,
                                     ),
                                     dbc.AccordionItem(
                                         title="Studies overview based on date",
                                         id="parametersItem2",
                                         children=parametersItem2
                                     ),
                                     dbc.AccordionItem(
                                         title="Studies repartition",
                                         id="parametersItem3",
                                         children=parametersItem3
                                     )
                                 ],
                                 style={
                                     "maxWidth": "20vmax",
                                     'fontSize': "0.6vmax"
                                 }
                             ),
                             html.Div(id="param1"),
                             html.Div(id="param2"),
                         ]),
             ],
             )

topAnimatedBanner = \
    dbc.Card(
        [
            dbc.CardImg(src="assets/img/category_style.svg", top=True,
                        style={
                            "borderRadius": "15px",
                            "transform": "rotate(180deg)"
                        }),
            dbc.CardImgOverlay(
                html.H2("Overview",
                        id="title",
                        className="outline",
                        style={
                            "color": "rgba(0,0,0,0)",
                            "textShadow": "-1px 0 white, 0 1px white, 1px 0 white, 0 -1px white",
                            "WebkitTextStroke": "20px"
                        }),
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "left",
                    "horizontalAlign": "center",
                    "marginLeft": "3vh"
                }
            ),
            dbc.CardImgOverlay(
                dbc.Button("Reset",
                           id="reset",
                           style={
                               'maxHeight': "2vmax"
                           }
                           ),
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "right",
                    "horizontalAlign": "center",
                    "marginLeft": "3vh"
                }
            ),
        ],
        style={"backgroundColor": "hsl(247.74, 52.54%, 98.43%)",
               "borderRadius": "15px"},
        class_name="card mb-4 border-0"
    )

barPlotByStudiesType = \
    dbc.Card(
        dbc.CardBody(
            [
                dcc.Graph(
                    id="studyTypeBar",
                    config={
                        'displayModeBar': False,
                    },
                    style={
                        "marginTop": "-1vh",
                        'height': '91vh',
                        "width": "10vw",
                    }
                ),
            ]
        ),
        id="SR_card",
        class_name="card mb-4 border-1",
        style={"backgroundColor": "hsl(247.74, 52.54%, 98.43%)",
               "borderRadius": "15px",
               }
    )

tabWithMultipleCharts = \
    dbc.Card(
        dbc.CardBody(
            [
                dcc.Tabs(id="pie-tabs",
                         value="tab1",
                         children=[
                             dcc.Tab(label="Category repartition",
                                     value="tab1",
                                     id="pieTab1",
                                     style=left_tab_style,
                                     selected_style=left_tab_selected_style,
                                     children=[
                                         dbc.Row([dcc.Graph(
                                             id="subCategoryProportion",
                                             style={
                                                 "width": "55vw",
                                                 "height": "40vh",
                                             },
                                             config={
                                                 "displayModeBar": False
                                             }
                                         )], justify="center"),
                                     ]
                                     ),

                             dcc.Tab(label="Category repartition by studies type",
                                     value="tab2",
                                     id="pieTab2",
                                     style=right_tab_style,
                                     selected_style=right_tab_selected_style,
                                     children=[
                                         dbc.Row([dcc.Graph(
                                             id="subCategoryProportionByStudiesType",
                                             style={
                                                 "width": "60vw",
                                                 "height": "40vh"
                                             },
                                             config={
                                                 "displayModeBar": False,
                                             }
                                         )], justify="center"),
                                     ]),
                         ],
                         style={
                             'height': '3vh',
                             "width": "60vw"
                         }
                         )
            ]
        ),
        id="CRP_card",
        class_name="card mb-4 border-1",
        style={"backgroundColor": "hsl(247.74, 52.54%, 98.43%)",
               "borderRadius": "15px"}
    )

studiesDateOverview = \
    dbc.Card(
        dbc.CardBody(
            [
                dcc.Tabs(
                    id="date-tabs",
                    value="tab1",
                    children=[
                        dcc.Tab(
                            label="Historical date overview",
                            value="tab1",
                            id="historicalTab1",
                            style=left_tab_style,
                            selected_style=left_tab_selected_style,
                            children=[
                                dcc.Graph(
                                    id="studiesDateEventByYear",
                                    style={
                                        "height": "37vh",
                                        "width": "60vw"
                                    },
                                    config={
                                        'displayModeBar': False,
                                    },
                                ),
                            ]
                        ),
                        dcc.Tab(
                            label="Historical studies overview",
                            value="tab2",
                            id="historicalTab2",
                            style=right_tab_style,
                            selected_style=right_tab_selected_style
                        )
                    ],
                    style={
                        'height': '3vh',
                        "width": "60vw"
                    }
                )
            ]
        ),
        id="SDO_card",
        class_name="card mb-4 border-1",
        style={"backgroundColor": "hsl(247.74, 52.54%, 98.43%)",
               "borderRadius": "15px",
               "marginTop": "-15px"}
    )
