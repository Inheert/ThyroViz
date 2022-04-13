import dash
from dash import dash_table

import pandas as pd
import dash_bootstrap_components as dbc

from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime

from pages.helpers import *

category = GetCategoryPercent(groupby="category", sortby=["nct_id"], sortasc=False)

callback_last_selected_button = None

card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
}

card_icon2 = {
    "color": "#454545",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
}

dash.register_page(__name__)

layout = html.Div(
    [
        dcc.Interval(interval=300 * 1000, id="refresh"),
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.CardGroup(
                                    [
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    html.H1(f"{len(studies['nct_id'].unique())}",
                                                            className="card-title"),
                                                    html.P("études uniques", className="card-text"),
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
                                                        f"{studies[(studies['study_first_submitted_date'] >= f'{datetime.now().year}-{datetime.now().month - 1}') & (studies['study_first_submitted_date'] < f'{datetime.now().year}-{datetime.now().month}')].shape[0]}",
                                                        className="card-title"),
                                                    html.P("nouvelles études ce mois-ci", className="card-text", ),
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
                                                        f"{len(sponsors.name.unique())}",
                                                        className="card-title"),
                                                    html.P("Nombre de sponsors",
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
                                                    html.P("Nombre d'investigateur",
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
                        ),
                    ],
                ),
                dbc.Row(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
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
                                                dbc.Card(
                                                    dbc.CardBody(
                                                        [
                                                            html.H2("GENERAL",
                                                                    style={
                                                                        "textAlign": "center",
                                                                        # "font-family": "Montserrat light",
                                                                        # "border": "1px black solid",
                                                                        # "border-radius": "0px",
                                                                        "borderColor": "black"
                                                                    }),
                                                        ]
                                                    ),
                                                    className="shadow p-3 mb-5 bg-white rounded"
                                                ),
                                                dcc.Graph(
                                                    id="study_type_bar",
                                                    config={
                                                        'displayModeBar': False,
                                                    },
                                                    style={
                                                        "width": "110vh",
                                                        "height": "10vh"
                                                    }
                                                ),
                                            ]
                                        )
                                    ],
                                    style={
                                        "display": "flex",
                                        "alignItems": "top",
                                        "justifyContent": "center",
                                        "horizontalAlign": "center"
                                    }
                                )
                            ],
                        ),
                    ],
                    style={
                        "margin": "auto",
                        "marginTop": "25px"
                    }
                )
            ],
        )
    ]
)


@callback(Output("study_type_bar", "figure"),
          [[Input(f"title-{category.loc[x]['category']}", "children"),
            Input(f"button-{category.loc[x]['category']}", "n_clicks")] for x in category.index],
          )
def AutoUpdateGraph(*args):
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

    colors = ['rgba(38, 24, 74, 0.8)', 'rgba(71, 58, 131, 0.8)',
              'rgba(122, 120, 168, 0.8)']

    x_data = [[x for x in df["nct_id"]]]

    y_data = [i for i in df["study_type"]]

    fig = go.Figure()

    for i in range(0, len(x_data[0])):
        for xd, yd in zip(x_data, y_data):
            fig.add_trace(go.Bar(
                x=[xd[i]], y=[yd],
                orientation='h',
                marker=dict(
                    color=colors[i],
                    line=dict(color='black', width=1)
                )
            ))

    fig.update_layout(
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
        paper_bgcolor='rgba(248, 248, 255, 0)',
        plot_bgcolor='rgba(248, 248, 255, 0)',
        margin=dict(l=80, r=0, t=0, b=0),
        showlegend=False,
        hovermode=False
    )

    annotations = []

    for yd, xd in zip(y_data, x_data):

        # labeling the first percentage of each bar (x_axis)
        annotations.append(dict(xref='x', yref='y',
                                x=xd[0] / 2, y=yd,
                                text=str(xd[0]) + '%',
                                font=dict(family='Arial', size=14,
                                          color='rgb(248, 248, 255)'),
                                showarrow=False))

        space = xd[0]
        for i in range(1, len(xd)):
            # labeling the rest of percentages for each bar (x_axis)
            annotations.append(dict(xref='x', yref='y',
                                    x=space + (xd[i] / 2), y=yd,
                                    text=str(xd[i]) + '%',
                                    font=dict(family='Arial', size=14,
                                              color='rgb(248, 248, 255)'),
                                    showarrow=False))

            space += xd[i]

    return fig

# @callback(Output("funnelCategory", "figure"),
#           Input("intervalRefresh", "n_intervals"))
# def autoRefreshFig(click):
#     df = studies[["nct_id", "category"]]
#     df = df.groupby("category").count().reset_index()
#     text = df["category"]
#
#     df.sort_values(by="nct_id", ascending=False, inplace=True)
#
#     fig = go.Figure(go.Funnelarea(
#         text=text,
#         values=df["nct_id"],
#         hoverinfo="none",
#     ))
#
#     fig.update_layout(
#         height=400,
#         margin=dict(
#             l=0,
#             r=0,
#             b=0,
#             t=0
#         ),
#         showlegend=False,
#         paper_bgcolor="rgba(0,0,0,0)",
#         autosize=True
#     )
#
#     return fig
