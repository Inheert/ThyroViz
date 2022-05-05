import dash_bootstrap_components as dbc
import dash_daq
import numpy as np
import pandas as pd
from dash import html, dcc, dash_table
import plotly.express as px

from pages.utilities.const import *
from pages.utilities.helpers import category

topCard1 = \
    dbc.CardGroup(
        [
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H1(f"{len(studies['nct_id'].unique())}",
                                className="card-title"),
                        html.P("studies in progress", className="card-text"),
                    ]
                )
            ),
            dbc.Card(
                html.Div(className="bi bi-eye", style=card_icon),
                color="#247cfd",
                style={"maxWidth": 75},
            ),
        ],
        className="mt-4 shadow",
    ),

topCard2 = \
    dbc.CardGroup(
        [
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H1(
                            f"{studies[(studies['study_first_submitted_date'] >= f'{datetime.now().year}-{datetime.now().month - 1}') & (studies['study_first_submitted_date'] < f'{datetime.now().year}-{datetime.now().month}')].shape[0]}",
                            className="card-title"),
                        html.P("new studies this month", className="card-text", ),
                    ]
                )
            ),
            dbc.Card(
                html.Div(className="bi bi-clipboard2-plus", style=card_icon),
                color="#0D6EFD",
                style={"maxWidth": 75},
            ),
        ],
        className="mt-4 shadow",
    )

topCard3 = \
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
                style={"maxWidth": 75},
            ),
        ],
        className="mt-4 shadow",
    )

topCard4 = \
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
                style={"maxWidth": 75},
            ),
        ],
        className="mt-4 shadow",
    )

DEPRECATED_leftCategoryCard = \
    [
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
                               color="primary",
                               outline=True)
                ],
            ),
            className="mb-1 shadow-sm"
        ) for x in category.index
    ]

leftCategoryCard = \
    dcc.Tabs(id="leftSideTab",
             value="tab1",
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
                                                    color="primary",
                                                    outline=True)
                                     ],
                                 ),
                                 className="mb-1 shadow-sm"
                             ) for x in category.index
                         ]
                         ),

                 dcc.Tab(label="Parameters",
                         value="tab2",
                         id="leftTab2",
                         style=tab_style,
                         selected_style=tab_selected_style,
                         children=[
                             html.Div(id="param1"),
                             html.Div(id="param2"),
                         ]),
             ],
             style={
                 "width": "300px"
             }
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
                           id="reset"),
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
                    }
                ),
                dash_daq.BooleanSwitch(
                    id="boolBarStudiesType",
                    on=False,
                    color="#0D6EFD"),
            ]
        ),
        class_name="card mb-4 border-0",
        style={"backgroundColor": "hsl(247.74, 52.54%, 98.43%)",
               "borderRadius": "15px"}
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
                                     style=tab_style,
                                     selected_style=tab_selected_style,
                                     children=[
                                         dcc.Graph(
                                             id="subCategoryProportion",
                                             config={
                                                 "displayModeBar": False
                                             }
                                         ),
                                         dbc.Row(
                                             [
                                                 dbc.Col(
                                                     dash_daq.BooleanSwitch(
                                                         id="boolCategoryRepartition",
                                                         on=False,
                                                         color="#0D6EFD"),
                                                     style={
                                                         "display": "flex",
                                                         "alignItems": "center",
                                                         "justifyContent": "right",
                                                         "horizontalAlign": "center",
                                                         "marginLeft": "3vh"
                                                     }
                                                 )
                                             ]
                                         )
                                     ]
                                     ),

                             dcc.Tab(label="Category repartition by studies type",
                                     value="tab2",
                                     id="pieTab2",
                                     style=tab_style,
                                     selected_style=tab_selected_style,
                                     children=[
                                         dcc.Graph(
                                             id="subCategoryProportionByStudiesType",
                                             config={
                                                 "displayModeBar": False,
                                             }
                                         ),
                                     ]),
                         ],
                         style=tabs_styles
                         )
            ]
        ),
        class_name="card mb-4 border-0",
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
                            style=tab_style,
                            selected_style=tab_selected_style,
                            children=[
                                dcc.Graph(
                                    id="studiesDateEventByYear",
                                    config={
                                        'displayModeBar': False,
                                    },
                                ),
                                dash_daq.BooleanSwitch(
                                    id="SDO_bool",
                                    on=False,
                                    color="#0D6EFD"),
                            ]
                        ),
                        dcc.Tab(
                            label="Historical studies overview",
                            value="tab2",
                            id="historicalTab2",
                            style=tab_style,
                            selected_style=tab_selected_style
                        )
                    ],
                    style=tabs_styles
                )
            ]
        ),
        class_name="card mb-4 border-0",
        style={"backgroundColor": "hsl(247.74, 52.54%, 98.43%)",
               "borderRadius": "15px"}
    )


def ModalStudiesInfo(row, isOpen):
    _s_base = s_base.sort_values(by="category")
    row = _s_base.loc[row].reset_index(drop=True)
    df = s_base[s_base["nct_id"] == row["nct_id"][0]].reset_index(drop=True).copy()
    sp = sponsors[sponsors["nct_id"] == row["nct_id"][0]]

    inv = investigators[investigators["nct_id"] == row["nct_id"][0]]

    loc = country[country["nct_id"] == row["nct_id"][0]]
    for col in row:
        row[col] = row[col].apply(lambda x: None if x is np.nan or x is pd.NaT or x is None else x)

    layout = \
        dbc.Modal(
            [
                dbc.ModalHeader(row.nct_id),
                dbc.ModalTitle(row.official_title if row.official_title[0] is not None else row.brief_title,
                               style={
                                   "fontSize": '25px',
                                   "fontWeight": "bold",
                                   "marginLeft": "5px"
                               }),
                dbc.ModalBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Markdown(f'''
                                        **Funded by:** {df.funded_bys.unique()[0]}
                                        \n
                                        **Study type:** {df.study_type.unique()[0]}
                                        \n
                                        **Overall status:** {df.overall_status.unique()[0]}
                                        \n
                                        **Study phases:** {df.study_phases.unique()[0]}
                                        \n
                                        **Minimum age:** {int(df.minimum_age_num.unique()[0])} years old
                                        \n
                                        **Maximum age:** {int(df.maximum_age_num.unique()[0])} years old
                                        \n
                                        **First submitted date:** {df.study_first_submitted_date[0].strftime("%Y-%m-%d")}
                                        \n
                                        **Estimated primary completion date:** {'Not provided' if df.primary_completion_date[0] is pd.NaT else df.primary_completion_date[0].strftime("%Y-%m-%d")}
                                        \n
                                        **Estimated completion date:** {'Not provided' if df.completion_date[0] is pd.NaT else df.completion_date[0].strftime("%Y-%m-%d")}
                                        ''')
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
                                        dcc.Graph(
                                            figure=px.scatter_geo(inv,
                                                                  locations="iso",
                                                                  color="continent",
                                                                  projection="orthographic")
                                        )
                                    ]
                                )
                            ],
                            style={
                                "display": "flex",
                                "alignItems": "center",
                                "justifyContent": "center",
                                "horizontalAlign": "center"
                            }
                        ),
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dash_table.DataTable(
                                            data=df.to_dict('records'),
                                            columns=[
                                                {"name": i, "id": i}
                                                for i in df[["category", "sub_category"]].columns
                                            ],
                                            style_data={
                                                "whiteSpace": "normal",
                                                "height": "auto"
                                            }
                                        )
                                    ],
                                    width="auto"
                                ),
                                dbc.Col(
                                    [
                                        dash_table.DataTable(
                                            data=sp.to_dict('records'),
                                            columns=[
                                                {"name": i, "id": i}
                                                for i in sp[["name", "lead_or_collaborator", "new_class"]]
                                            ],
                                            style_data={
                                                "whiteSpace": "normal",
                                                "height": "auto"
                                            }
                                        ),
                                        html.Br(),
                                        dash_table.DataTable(
                                            data=inv.to_dict('records'),
                                            columns=[
                                                {"name": i, "id": i}
                                                for i in inv[["name"]]
                                            ],
                                            style_data={
                                                "whiteSpace": "normal",
                                                "height": "auto"
                                            }
                                        )
                                    ],
                                    width="auto"
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                    ],
                                    width="auto"
                                )
                            ]
                        )
                    ]
                )
            ],
            id="studyModal",
            is_open=isOpen,
            size="xl"
        )

    return layout
