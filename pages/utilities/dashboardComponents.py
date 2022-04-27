import dash_bootstrap_components as dbc
from dash import html, dcc
import dash_daq as daq
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
                            f"{len(investigators.investigators.unique())}",
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

leftCategoryCard = \
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
                                     id="Pietab1",
                                     style=tab_style,
                                     selected_style=tab_selected_style,
                                     children=[
                                         dcc.Graph(
                                             id="subCategoryProportion",
                                             config={
                                                 "displayModeBar": False
                                             }
                                         )
                                     ]
                                     ),

                             dcc.Tab(label="Category repartition by studies type",
                                     value="tab2",
                                     id="Pietab2",
                                     style=tab_style,
                                     selected_style=tab_selected_style,
                                     children=[
                                         dcc.Graph(
                                             id="subCategoryProportionByStudiesType",
                                             config={
                                                 "displayModeBar": False,
                                             }
                                         )
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
