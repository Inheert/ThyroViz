import dash_bootstrap_components as dbc
from dash import html

from const import *

topCard1 = dbc.CardGroup(
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

topCard2 = dbc.CardGroup(
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

topCard3 = dbc.CardGroup(
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

topCard4 = dbc.CardGroup(
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
