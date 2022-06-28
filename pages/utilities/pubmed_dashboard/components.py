from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import dash_daq as daq
from datetime import datetime

from pages.utilities.pubmed_const import *

topCard1 = \
    dbc.CardGroup(
        [
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H1(f"{articles['PMID'].nunique()}",
                                className="card-title"),
                        html.P("Total articles", className="card-text"),
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
    )

topCard2 = \
    dbc.CardGroup(
        [
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H1(
                            f"{articles[(articles['Entrez_date'] >= f'{datetime.now().year}-{datetime.now().month - 1}') & (articles['Entrez_date'] < f'{datetime.now().year}-{datetime.now().month}')].shape[0]}",
                            className="card-title"),
                        html.P("new articles this month", className="card-text", ),
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
    )

topCard3 = \
    dbc.CardGroup(
        [
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H1(f"{full_author_name['Full_author_name'].nunique()}",
                                className="card-title"),
                        html.P("Total authors", className="card-text"),
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
    )

general_filters = \
    dbc.Card(
        dbc.CardBody(
            [
                html.H5("Filters applicable to all graphs:", style={"textAlign": "center"}),
                dbc.Row([
                    dbc.Col([
                        html.Plaintext("Publication type:"),
                        dcc.Dropdown(
                            id="publication_type",
                            options=all_p_type,
                            value=[],
                            multi=True,
                        )
                    ]),
                    dbc.Col([
                        html.Plaintext("Authors name:"),
                        dcc.Dropdown(
                            id="author",
                            options=all_authors,
                            value=[],
                            multi=True,
                        )
                    ]),
                    dbc.Col([
                        html.Plaintext("Population:"),
                        dcc.Dropdown(
                            id="population",
                            options=all_population,
                            value=[],
                            multi=True,
                        )
                    ]),
                ])
            ]
        ),
        class_name="card mb-4 border-1 shadow",
        style={"backgroundColor": "hsl(247.74, 52.54%, 98.43%)",
               "borderRadius": "15px",
               "marginTop": "-15px"}
    )

categoryRepartition = \
    dbc.Card(
        dbc.CardBody(
            [
                dcc.Graph(
                    id="categoryRepartition",
                    style={
                        "width": "35vw",
                        "height": "40vh",
                    },
                    config={
                        "displayModeBar": False,
                    }
                )
            ]
        ),
        class_name="card mb-4 border-1 shadow",
        style={"backgroundColor": "hsl(247.74, 52.54%, 98.43%)",
               "borderRadius": "15px",
               "marginTop": "-15px"}
    )

articlesDateOverview = \
    dbc.Card(
        dbc.CardBody([
            dcc.Graph(
                id="articleDateOverview",
                style={
                    "height": "40vh",
                    "width": "55vw",
                    "margin": "1em"
                },
                config={
                    'displayModeBar': False,
                },
            ),

            html.Br(),

            dbc.Accordion([
                dbc.AccordionItem(title="Filters",
                                  children=[
                                      dbc.Row([
                                          dbc.Col([
                                              html.Plaintext("Frequency:"),
                                              dcc.RadioItems(id="dateFrequency",
                                                             options=["Year", "Month"],
                                                             value="Year")
                                          ], width="auto"),
                                          dbc.Col([
                                              dbc.Row([
                                                  html.Plaintext("Year range:", style={"textAlign": "center"}),
                                                  dbc.Col(
                                                      daq.NumericInput(
                                                          id="dateMin",
                                                          min=1999,
                                                          max=datetime.now().year - 1,
                                                          value=2000,
                                                          size=65
                                                      ),
                                                      style={
                                                          "display": "flex",
                                                          "alignItems": "center",
                                                          "justifyContent": "center",
                                                          "horizontalAlign": "center",
                                                      },
                                                      width="auto"
                                                  ),
                                                  dbc.Col(html.Plaintext("to"),
                                                          style={
                                                              "display": "flex",
                                                              "alignItems": "end",
                                                              "verticalAlign": "bottom",
                                                          },
                                                          width="auto"),
                                                  dbc.Col(
                                                      daq.NumericInput(
                                                          id="dateMax",
                                                          min=2000,
                                                          max=datetime.now().year,
                                                          value=datetime.now().year,
                                                          size=65
                                                      ),
                                                      style={
                                                          "display": "flex",
                                                          "alignItems": "center",
                                                          "justifyContent": "center",
                                                          "horizontalAlign": "center",
                                                      },
                                                      width="auto"
                                                  )
                                              ], justify="center"),
                                          ], width="auto"),
                                          dbc.Col(
                                              [
                                                  dcc.Checklist(
                                                      id="date_checklist",
                                                      options=["Show graph by conditions"],
                                                      inputStyle={
                                                          "marginRight": "6px"
                                                      }
                                                  )
                                              ]
                                          )
                                      ], align="center"),

                                      html.Br(),

                                      html.Plaintext("Conditions:"),
                                      dcc.Dropdown(
                                          id="dateCondition",
                                          options=[x for x in all_conditions],
                                          value=[],
                                          multi=True,
                                          style={
                                              "maxWidth": "50vmax"
                                          }
                                      )
                                  ])
            ],
                style={"borderRadius": "15px"},
                start_collapsed=False
            )
        ]),
        class_name="card mb-4 border-1 shadow",
        style={"backgroundColor": "hsl(247.74, 52.54%, 98.43%)",
               "borderRadius": "15px",
               "marginTop": "-15px"}
    )
