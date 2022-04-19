import dash
from dash import dcc, Input, Output, callback, html
import dash_bootstrap_components as dbc

dash.register_page(__name__)

layout = html.Div(
    [
        html.H2("Questions"),
        html.Plaintext("Sur quoi baser les différentes stats, l'ensemble des études ou un type d'étude en particulier"),
        html.Plaintext("Qu'elles sont les éléments nécessitant un accès aux modifs simplifié"),
        html.Br(),
        html.H2("A faire"),
        html.Plaintext("nettoyer les dernières sous-catégorie des classifications inutiles"),
        html.Plaintext("Finir la vue générale cette semaine (22/04)")
    ]
)
