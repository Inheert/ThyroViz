import dash
from dash import dcc, Input, Output, callback, html
import dash_bootstrap_components as dbc

import plotly.graph_objects as go
from datetime import datetime

from pages.helpers import *
from pages.const import *

dash.register_page(__name__)

layout = html.Div(
    [
        dcc.Interval(interval=300 * 1000, id="refresh"),

        html.Div(
            [
                dbc.Row(
                    # Cette séction comporte les 4 cartes présentent en haut de page
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
                            width=3
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
                            width=3
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
                                            html.H5(f"{category.loc[x]['category']}",
                                                    className="card-title",
                                                    id=f"title-{category.loc[x]['category']}"),
                                            html.P(
                                                f"{category.loc[x]['nct_id']}%"
                                            ),
                                            dbc.Button(children="Développer",
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
                                                            html.H2("Général",
                                                                    id="title",
                                                                    className="outline",
                                                                    style={
                                                                        "color": "rgba(0,0,0,0)",
                                                                        "textShadow": "-1px 0 white, 0 1px white, 1px 0 white, 0 -1px white",
                                                                        "webkit-text-stroke": "20px"
                                                                    }),
                                                            style={
                                                                "display": "flex",
                                                                "alignItems": "center",
                                                                "justifyContent": "left",
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
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    dcc.Graph(
                                                        id="study_type_bar",
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
                )
            ],
        )
    ],
    style={
        # "overflow": "scroll"
    }
)


@callback(Output("study_type_bar", "figure"),
          Output("title", "children"),
          [[Input(f"title-{category.loc[x]['category']}", "children"),
            Input(f"button-{category.loc[x]['category']}", "n_clicks")] for x in category.index],
          )
def VisualizationDataUpdate(*args):
    category_selected = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if category_selected != ".":
        category_selected = category_selected.split("-")[1].split(".")[0]
        df = GetCategoryPercent(columns=["study_type"], groupby=["category", "study_type"],
                                sortby=["category", "nct_id"],
                                sortasc=False, divisionby="selection", categoryfilter=category_selected)
    else:
        df = GetCategoryPercent(columns=["study_type"], groupby=["category", "study_type"],
                                sortby=["category", "nct_id"],
                                sortasc=False)
        df = df[df["category"] == "Thyroid neoplasms"]

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

    return fig, category_selected if category_selected != "." else "Général"
