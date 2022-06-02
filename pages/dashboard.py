import dash
from dash import Input, Output, callback
from plotly.subplots import make_subplots

from pages.utilities.dashboard.components import *
from pages.utilities.dashboard.graphParameters import *
from pages.utilities.dashboard.callbacks import *

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
                            topCardNav1,
                            width=True
                        ),
                        html.H2("caca"),
                        dbc.Col(
                            topCardNav2,
                            width=True
                        ),
                        dbc.Col(
                            topCardNav3,
                            width=True
                        ),
                        dbc.Col(
                            topCardNav4,
                            width=True
                        ), ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            leftCategoryCard,
                            width="auto"
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        dbc.Row(
                                            dbc.Col(
                                                topAnimatedBanner,
                                                width="auto"
                                            )
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        lightStatistic1,
                                                    ],
                                                    width="auto"
                                                ),
                                                dbc.Col(
                                                    [
                                                        lightStatistic2
                                                    ],
                                                    width="auto"
                                                ),
                                            ],
                                            align="center", justify="center"
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(
                                                                    tabWithMultipleCharts,
                                                                    width="auto",
                                                                )
                                                            ]
                                                        ),
                                                        html.Br(),
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(
                                                                    [
                                                                        studiesDateOverview
                                                                    ],
                                                                    style={
                                                                        "display": "flex",
                                                                        "alignItems": "top",
                                                                        "justifyContent": "right",
                                                                        "horizontalAlign": "center",
                                                                    },
                                                                    width="auto"
                                                                )
                                                            ]
                                                        ),
                                                    ],
                                                    width="auto"
                                                ),
                                                dbc.Col(
                                                    barPlotByStudiesType,
                                                    width="auto",
                                                ),
                                            ],
                                            justify="center",
                                        ),
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
                dbc.Row(
                    studiesDatatable
                ),

                dcc.Store(id="studyIndex"),
                html.Div(
                    ModalStudiesInfo([0], False),
                    id="studiesModal"
                ),

                dcc.Store(id="selected-card"),
            ],
        )
    ],
    style={
        # "overflow": "scroll"
    }
)
