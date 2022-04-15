import dash_bootstrap_components as dbc
from dash import html, dcc
from datetime import datetime

from pages.helpers import *

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

category = GetCategoryPercent(groupby="category", sortby=["nct_id"], sortasc=False)

topCard = [
    dbc.Col(
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
                                html.P("nouvelles études ce mois", className="card-text", ),
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
    ), ]

categoryCard = dbc.Col(
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
)
