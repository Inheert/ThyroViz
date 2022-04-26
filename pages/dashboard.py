import dash
from dash import dcc, Input, Output, callback, html
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots

from pages.utilities.helpers import *
from pages.utilities.const import *

""""
Idées graphiques :
                - Distribution des catégories d'études par type d'étude / date
                - Distribution des sous-catégories d'études par type d'étude / date
                - Evolution du nombre d'études par rapport à N-1 par catégorie --> sous-catégorie
                - Mise en avant des études les plus récentes
                - Mise en avant des études ayant une date de complétion proche
                - Mise en avant des plus grosse fondations d'études
                - Mise en avant des sponsors les plus important sur l'ensemble des études / par catégorie
                - Représentation géographique des études à travers le monde 
                - Classification des études par les tranches d'âges acceptées
                - Classification des études par leur status
                - Classification des études par phase
                - Moyenne des études par mois / années
                - Nombre d'étude déjà achevé 
                - Nombre d'étude avec une première complétion
                - Nombre de nouvelles études depuis le début d'année
"""""

tabs_styles = {
    'height': '44px',
    "width": "1000px"
}
tab_style = {
    "display": "flex",
    "justify-content": "center",
    "align-items": "center",
    'borderBottom': '1px solid #d6d6d6',
    'fontWeight': 'bold'
}

tab_selected_style = {
    "display": "flex",
    "justify-content": "center",
    "align-items": "center",
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
}

dash.register_page(__name__)

layout = html.Div(
    [
        dcc.Store(id="category_button"),

        dcc.Interval(interval=10 * 1000, id="refresh"),

        html.Div(
            [
                dbc.Row(
                    # Cette section comporte les 4 cartes présentent en haut de page
                    [
                        dbc.Col(
                            dbc.CardGroup(
                                [
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.H1(f"{len(studies['nct_id'].unique())}",
                                                        className="card-title"),
                                                html.P("unique studies", className="card-text"),
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
                            width=True
                        ),
                        dbc.Col(
                            [
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
                            ],
                            width=True
                        ),
                        dbc.Col(
                            [
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
                                ),
                            ],
                            width=True
                        ),
                        dbc.Col(
                            [
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
                                ),
                            ],
                            width=True
                        ), ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            # Colonne contenant les cards-buttons sur la partie gauche de la page.
                            # Celles-ci sont générées automatiquement à l'aide d'une compréhension de liste
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
                            ],
                            width="auto"
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        dbc.Row(
                                            # Cette ligne contient l'en-tête de la visualisation (bannière animé +
                                            # titre)
                                            [
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
                                                )]
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
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
                                                            style={"backgroundColor": "rgb(247, 247, 247)",
                                                                   "borderRadius": "15px",
                                                                   "width": "18vh",
                                                                   "height": "86vh",
                                                                   },
                                                            class_name="card mb-4 border-0"
                                                        ),
                                                    ],
                                                    width="auto"
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Row(
                                                            [
                                                                html.H3("Category / Sub-category repartition:",
                                                                        id="tabPieTitle",
                                                                        style={
                                                                            "textAlign": "center",
                                                                        }),
                                                                dbc.Col(
                                                                    [
                                                                        dcc.Tabs(id="pie-tabs", value="tab1", children=[
                                                                            dcc.Tab(label="No filter",
                                                                                    value="tab1",
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

                                                                            dcc.Tab(label="By studies type",
                                                                                    value="tab2",
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
                                                                                 ),

                                                                    ],
                                                                    style={
                                                                        "display": "flex",
                                                                        "alignItems": "center",
                                                                        "justifyContent": "center",
                                                                        "horizontalAlign": "center",
                                                                    },
                                                                    width=True
                                                                )
                                                            ]
                                                        ),
                                                        dbc.Row(
                                                            [
                                                                html.Plaintext("Age range")
                                                            ],
                                                            justify="center", align="center",
                                                            style={
                                                                "textAlign": "center"
                                                            }
                                                        ),
                                                        dbc.Row(
                                                            [
                                                                dcc.RangeSlider(min=0,
                                                                                max=100,
                                                                                step=5,
                                                                                value=[0, 100],
                                                                                id="age_range_slider")
                                                            ]
                                                        ),
                                                        html.Br(),
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(
                                                                    [
                                                                        dcc.Graph(
                                                                            id="studiesDateEventByYear",
                                                                            config={
                                                                                'displayModeBar': False,
                                                                            },
                                                                        )
                                                                    ],
                                                                    style={
                                                                        "display": "flex",
                                                                        "alignItems": "top",
                                                                        "justifyContent": "center",
                                                                        "horizontalAlign": "center",
                                                                    },
                                                                    width=True
                                                                )
                                                            ]
                                                        ),
                                                    ],
                                                ),
                                            ]
                                        )
                                    ]
                                )
                            ],
                            style={
                                "display": "flex",
                                "alignItems": "top",
                                "justifyContent": "center",
                                "horizontalAlign": "center",
                            }
                        )

                    ],
                    style={
                        "margin": "auto",
                        "marginTop": "25px"
                    }
                ),
                dcc.Store(id="selected-card")
            ],
        )
    ],
    style={
        # "overflow": "scroll"
    }
)

"""
########################################################################################################################
THIS CALLBACK UPDATE STORE COMPONENT USED TO DEFINE
IF A CATEGORY HAS BEEN SELECTED OR NOT
OR IF THE RESET BUTTON IS SELECTED
########################################################################################################################
"""
@callback(Output("selected-card", "data"),
          Input("reset", "n_clicks"),
          [Input(f"button-{category.loc[x]['category']}", "n_clicks") for x in category.index])
def StoredDataUpdate(data, *args):
    trigger_button = [p['prop_id'] for p in dash.callback_context.triggered][0]

    try:
        trigger_button = trigger_button.split("-")[1].split(".")[0]

        if trigger_button in all_category:
            return trigger_button
        else:
            return data
    except IndexError:
        if trigger_button == "reset.n_clicks":
            return None
        else:
            return data


"""
########################################################################################################################
THIS CALLBACK IS USED TO UPDATES ALL TEXT COMPONENT 
########################################################################################################################
"""
@callback(Output("title", "children"),
          Output("tabPieTitle", "children"),
          Input("selected-card", "data"))
def TextUpdate(data):
    if data in all_category:
        return data, "Sub-category repartition:"
    else:
        return "Overview", "Category repartition:"


"""
########################################################################################################################
THIS CALLBACK IS USED TO UPDATE THE VERTICAL BAR CHART BY STUDY_TYPE
########################################################################################################################
"""
@callback(Output("studyTypeBar", "figure"),
          Input("selected-card", "data"))
def BarChartUpdate(data):
    if data in all_category:
        df = GetCategoryPercent(columns=["study_type"],
                                groupby=["category", "study_type"],
                                sortby=["category", "nct_id"],
                                sortasc=False,
                                divisionby="selection",
                                categoryfilter=data)
    else:
        df = GetCategoryPercent(columns=["study_type"],
                                groupby=["study_type"],
                                sortby=["category", "nct_id"],
                                sortasc=False)
        df["category"] = "All"

    s_type = [x for x in df["study_type"]]
    marker_color = ["#342883", "#4a39bb", "#6f60cf"]

    fig = go.Figure(data=[
        go.Bar(name="Interventional",
               x=df[df["study_type"] == y]["category"],
               y=df[df["study_type"] == y]["nct_id"],
               text=f"{df[df['study_type'] == y]['study_type'].iloc[0]}<br>{df[df['study_type'] == y]['percent'].iloc[0]}",
               insidetextanchor="middle",
               marker=dict(color=marker_color[x],
                           line=dict(width=2, color="white")),
               )
        for x, y in enumerate(s_type)])

    fig.update_layout(
        height=800,
        width=150,
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            constrain="domain"
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        barmode='stack',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        hovermode=False
    )

    return fig


"""
########################################################################################################################
THIS CALLBACK IS USED TO UPDATE THE PIE CHART FROM THE "NO FILTER" TAB
########################################################################################################################
"""
@callback(Output("subCategoryProportion", "figure"),
          Input("selected-card", "data"),
          Input("age_range_slider", "value"))
def pieNoFilterUpdate(data, age_range):
    age_range = list((map(lambda x: int(float(x)), age_range)))
    df = GetSubCategoryProportion(data, None, age_range)
    fig = go.Figure(data=[go.Pie(
        labels=df["view"],
        values=df["nct_id"],
        marker=dict(
            colors=df["color"]
        )
    )])

    fig.update_traces(hole=.4, hoverinfo="label+percent")

    fig.update_layout(
        height=290,
        width=900,
        xaxis=dict(
            showgrid=False,
            showline=False,
            zeroline=False,
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=True,
        legend=dict(
            x=1.1,
            itemclick=False,
            # orientation="v",
            # font=dict(
            #     size=8
            # )
        )
    )
    return fig


"""
########################################################################################################################
THIS CALLBACK IS USED TO UPDATES PIES CHARTS FROM THE "BY STUDIES TYPE" TAB
########################################################################################################################
"""
@callback(Output("subCategoryProportionByStudiesType", "figure"),
          Input("selected-card", "data"),
          Input("age_range_slider", "value"))
def pieByStudiesTypeUpdate(data, age_range):
    fig = make_subplots(rows=1, cols=3, specs=[[{"type": "domain"},
                                                {"type": "domain"},
                                                {"type": "domain"}]])

    col = 1
    for i in s_base.study_type.sort_values().unique():
        df = GetSubCategoryProportion(data, i, age_range)

        fig.add_trace(
            go.Pie(
                labels=df["view"],
                values=df["nct_id"],
                title=i,
                marker=dict(
                    colors=df["color"]
                )
            ),
            1, col)

        col += 1

    fig.update_traces(hole=.4,
                      hoverinfo="label+percent")

    fig.update_layout(
        height=290,
        width=900,
        xaxis=dict(
            showgrid=False,
            showline=False,
            zeroline=False,
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=True,
        legend=dict(
            x=1.1,
            itemclick=False,
            # orientation="v",
            # font=dict(
            #     size=8
            # )
        )
    )
    return fig


"""
########################################################################################################################
THIS CALLBACK IS USED TO UPDATE THE LINE CHART WITH NEW AND COMPLETED STUDIES
########################################################################################################################
"""
@callback(Output("studiesDateEventByYear", "figure"),
          Input("selected-card", "data"))
def LinePlotByYearUpdate(data):
    fig = go.Figure(data=StudiesByYear(data))

    fig.update_layout(
        height=250,
        width=950,
        title={
            'text': 'New and completed studies by year',
            'y': 0.9,
            'x': 0.5,
            "xanchor": "center",
            "yanchor": "top"
        },
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=True,
            color='black',
            zeroline=False,
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
    )
    return fig

# @callback(Output("category_button", "data"),
#           Input("category_button", "data"),
#           Input("reset", "n_clicks"),
#           [[Input(f"title-{category.loc[x]['category']}", "children"),
#             Input(f"button-{category.loc[x]['category']}", "n_clicks")] for x in category.index],
#           )
# def VisualizationDataUpdate(data, range, *args):
#     category_selected = [p['prop_id'] for p in dash.callback_context.triggered][0]
#
#     data = None if category_selected == "reset.n_clicks" else data
#
#     category_selected = "." if category_selected in ["reset.n_clicks", "age_range_slider.value"] else category_selected
#
#     data = category_selected if category_selected != "." else data
#
#     color_pie = ["hsl(185.23, 100%, 52.75%)",
#                  "hsl(201.22, 95.82%, 53.14%)",
#                  "hsl(216.05, 100%, 55.29%)",
#                  "hsl(230.67, 98.25%, 55.1%)",
#                  "hsl(243.98, 100%, 55.69%)",
#                  "hsl(244.41, 100%, 86.67%)",
#                  "hsl(258.18, 78.2%, 58.63%)",
#                  "hsl(258, 77.78%, 35.29%)"]
#
#     news_and_completed_study_by_year = go.Figure(data=StudiesByYear(category_selected))
#
#     news_and_completed_study_by_year.update_layout(
#         height=250,
#         width=950,
#         title={
#             'text': 'New and completed studies by year',
#             'y': 0.9,
#             'x': 0.5,
#             "xanchor": "center",
#             "yanchor": "top"
#         },
#         xaxis=dict(
#             showgrid=False,
#             showline=False,
#             showticklabels=True,
#             color='black',
#             zeroline=False,
#         ),
#         yaxis=dict(
#             showgrid=False,
#             showline=False,
#             showticklabels=False,
#             zeroline=False,
#         ),
#         paper_bgcolor='rgba(0, 0, 0, 0)',
#         plot_bgcolor='rgba(0, 0, 0, 0)',
#         margin=dict(l=0, r=0, t=0, b=0),
#         showlegend=False,
#     )
#
#     return data
