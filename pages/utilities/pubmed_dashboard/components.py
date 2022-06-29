from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import dash_daq as daq
from datetime import datetime, date

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
                                                  initial_visible_month=date(2000, 1, 1),
                                                  end_date=date(datetime.now().year + 1, 12, 31)),
                                              html.Br(style={"marginTop": "2vh"}),
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
                                      ),
                                      dcc.Checklist(
                                          id="selectAllCategory",
                                          options=["Select all category"],
                                          inputStyle={"marginRight": "6px"}
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
