from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import dash_daq as daq
from datetime import datetime, date, timedelta

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
                    ]),
                    dbc.Col([
                        html.Plaintext("Authors name:"),
                    ]),
                    dbc.Col([
                        html.Plaintext("Population:"),
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
                                                             options=["Year", "Month", "Weekly", "Day"],
                                                             value="Year",
                                                             inputStyle={
                                                                 "marginRight": "6px"
                                                             })
                                          ],
                                              width="auto"),

                                          dbc.Col([
                                              html.Plaintext("Year range:"),
                                              dcc.DatePickerRange(
                                                  id="datePickerRange",
                                                  min_date_allowed=date(2000, 1, 1),
                                                  max_date_allowed=date(datetime.now().year + 1, 12, 31),
                                                  start_date=date(2000, 1, 1),
                                                  end_date=date(datetime.now().year + 1, 12, 31)),
                                              html.Br(style={"marginTop": "0vh"}),
                                              dcc.Checklist(
                                                  id="date_checklist",
                                                  options=["Show graph by conditions"],
                                                  inputStyle={
                                                      "marginRight": "6px"
                                                  }
                                              )
                                          ],
                                              width="auto",
                                              style={
                                                  "marginLeft": "2vw",
                                              }),

                                      ], align="start"),
                                  ])
            ],
                style={"borderRadius": "15px"},
                start_collapsed=True
            )
        ]),
        class_name="card mb-4 border-1 shadow",
        style={"backgroundColor": "hsl(247.74, 52.54%, 98.43%)",
               "borderRadius": "15px",
               "marginTop": "-15px"}
    )


dateGraphKPI = \
    dbc.Card(
        dbc.CardBody(
            [
                dbc.Row(
                    [
                        html.H5("Statistics", style={"textAlign": "center"})
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.P("Average:", id="stat_average"),
                            ]
                        )
                    ]
                )
            ]
        ),
        class_name="card mb-4 border-1 shadow",
        style={"backgroundColor": "hsl(247.74, 52.54%, 98.43%",
               "borderRadius": "15px",
               }
    )

accordionArticles = \
    dbc.Card(
        dbc.CardBody(
            [
                dbc.Row(
                    [
                        dcc.Checklist(id="onlyObservational",
                                      options=["Only show observational articles"],
                                      value=[],
                                      inputStyle={
                                          "marginRight": "6px"
                                      }
                                      ),
                        html.Br(),

                        dbc.Col(
                            [
                                dbc.Input(id="articles_input",
                                          placeholder="Search text...",
                                          size="lg",
                                          class_name="mb-3"),
                                dcc.Checklist(id="articles_search_col",
                                              options=["Abstract", "Title", "Mesh_terms", "Other_terms", "Condition", "Chemical"],
                                              value=["Abstract"],
                                              inputStyle={"marginRight": "6px",
                                                          "marginLeft": "20px"},
                                              inline=True)
                            ],
                            width=4,
                            style={
                                "display": "block",
                                "alignItems": "center",
                                "justifyContent": "left",
                            }
                        ),
                        dbc.Col(
                            [
                                dcc.Dropdown(
                                    id="publication_type",
                                    options=all_p_type,
                                    value=[],
                                    placeholder="Select publication type...",
                                    multi=True,
                                ),

                                html.Br(),

                                dcc.Dropdown(
                                    id="population",
                                    options=all_population,
                                    value=[],
                                    placeholder="Select population group...",
                                    multi=True,
                                ),
                            ]
                        ),
                        dbc.Col(
                            [
                                dcc.Dropdown(
                                    id="dateCategory",
                                    options=[x for x in all_category],
                                    value=[],
                                    multi=True,
                                    placeholder="Select category...",
                                ),

                                html.Br(),

                                dcc.Dropdown(
                                    id="observational_type",
                                    options=[x for x in all_obs_value],
                                    value=[],
                                    multi=True,
                                    disabled=True,
                                    placeholder="Select observational characteristics",
                                )
                            ]
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        dbc.Pagination(
                                            id="articles_pagination",
                                            fully_expanded=False,
                                            max_value=5
                                        ),

                                        html.Br(),

                                        html.Button(id="download_button", children="Download excel")
                                    ],
                                    style={"float": "right",
                                           "alignItems": "center",
                                           }
                                ),
                            ],
                            width=True,
                        )
                    ],
                ),
                html.Br(style={"marginTop": "10px"}),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(id="accordionArticles")
                            ]
                        ),
                    ]
                ),
            ]
        ),
        class_name="card mb-4 border-1 shadow",
        style={"backgroundColor": "hsl(247.74, 52.54%, 98.43%)",
               "borderRadius": "15px"}
    )
