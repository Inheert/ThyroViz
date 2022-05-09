import dash_bootstrap_components as dbc
import dash_daq
import numpy as np
import pandas as pd
from dash import html, dcc, dash_table
import plotly.express as px
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import plotly.graph_objects as go

from pages.utilities.const import *
from pages.utilities.helpers import category
from pages.utilities.dashboardParameters import *

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

lightStatistics = \
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
                                    html.Div(
                                        id="card1Output1",
                                        style={
                                            "fontSize": 20
                                        },
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
                                            id="card1Output2",
                                            ),
                                    width="auto"
                                ),
                            ]
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
                                    html.P("compared to: ",
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
                                    style={
                                    }
                                ),
                                dbc.Col(
                                    [
                                        html.Div(
                                            className="bi bi-question-circle",
                                            id="cardInfo1",
                                            style={
                                                "fontSize": 15
                                            }
                                        ),
                                        dbc.Popover(
                                            dbc.PopoverBody(
                                                children="Compare the new studies this year to N-X\n"
                                                         "(N is the actual year, X is the selected number)."
                                                         "\n\n"
                                                         "To calculate this field we do a evolution rate.\n"
                                                         "With: starting value: first box\n"
                                                         "            arrival value: second box"
                                                         "\n\n"
                                                         "If any of the selections is equal to actual year\n"
                                                         "then the studies taken into account have a date\n"
                                                         "less than or equal to the current day and month.",
                                                style={
                                                    "whiteSpace": 'pre'
                                                }
                                            ),
                                            target="cardInfo1",
                                            body=True,
                                            trigger="hover"
                                        )
                                    ]
                                    ,
                                    width="auto",
                                    style={
                                        "display": "flex",
                                        "alignItems": "center",
                                    }
                                )
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
                                 className="mb-1 shadow-sm",
                                 style={
                                     "backgroundColor": "rgba(0,0,0,0)"
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
                                         children=parametersItem1
                                     ),
                                     dbc.AccordionItem(
                                         title="Studies overview based on date",
                                         id="parametersItem2",
                                         children=parametersItem2
                                     )
                                 ]
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
        class_name="card mb-4 border-1",
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
                                     style=left_tab_style,
                                     selected_style=left_tab_selected_style,
                                     children=[
                                         dcc.Graph(
                                             id="subCategoryProportion",
                                             config={
                                                 "displayModeBar": False
                                             }
                                         ),
                                     ]
                                     ),

                             dcc.Tab(label="Category repartition by studies type",
                                     value="tab2",
                                     id="pieTab2",
                                     style=right_tab_style,
                                     selected_style=right_tab_selected_style,
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
                    style=tabs_styles
                )
            ]
        ),
        style={"backgroundColor": "hsl(247.74, 52.54%, 98.43%)",
               "borderRadius": "15px",
               "marginTop": "-15px"}
    )


def ModalStudiesInfo(row, isOpen):
    _s_base = s_base.sort_values(by="category")
    row = _s_base.loc[row].reset_index(drop=True)
    df = s_base[s_base["nct_id"] == row["nct_id"][0]].reset_index(drop=True).copy()
    sp = sponsors[sponsors["nct_id"] == row["nct_id"][0]]

    inv = investigators[investigators["nct_id"] == row["nct_id"][0]].__deepcopy__()
    inv["city_country"] = inv[["city", "country"]].agg(", ".join, axis=1)

    geoloc = Nominatim(user_agent="ThyroResearch", timeout=3)

    inv["lat"] = inv["city_country"].apply(lambda x: geoloc.geocode(x).latitude)
    inv["long"] = inv["city_country"].apply(lambda x: geoloc.geocode(x).longitude)

    for col in row:
        row[col] = row[col].apply(lambda x: None if x is np.nan or x is pd.NaT or x is None else x)

    data = [go.Scattergeo(
        lat=inv["lat"],
        lon=inv["long"],
        text=inv["name"],
        mode="markers",
        hovertemplate=
        "<b>%{text}</b><br><br>"
    )]

    layout = go.Layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=350,
        width=350,
        showlegend=False,
        geo=go.layout.Geo(
            projection=dict(type="orthographic"),
            showland=True,
            showcountries=True
        )
    )

    fig = go.Figure(data=data, layout=layout)

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
                                            figure=fig,
                                            config={
                                                'displayModeBar': False,
                                            }
                                        ),
                                    ],
                                    style={
                                        "marginLeft": "20px",
                                        "display": "flex",
                                        "alignItems": "center",
                                        "justifyContent": "center",
                                        "horizontalAlign": "center"
                                    }
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


studiesDatatable = \
    dash_table.DataTable(
        id="datatable",
        data=s_base.to_dict('records'),
        columns=[{"name": i, "id": i} for i in
                 s_base[["nct_id", "category", "sub_category", "study_first_submitted_date",
                         "primary_completion_date", "completion_date", "study_type",
                         "overall_status", "study_phases", "minimum_age_num",
                         "maximum_age_num"]].columns],
        page_size=40,
        filter_action="native",
        sort_action="native",
        row_selectable="single",
        style_header={
            'backgroundColor': "white"
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
