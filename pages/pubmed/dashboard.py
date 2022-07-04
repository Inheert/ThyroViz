import dash
from script.pubmed.PubmedGroup import *
from pages.utilities.pubmed_dashboard.callbacks import *

dash.register_page(__name__)

layout = html.Div([
    dcc.Interval(id="first_interval"),
    dbc.Row(
        [
            dbc.Col(topCard1, width=2),
            dbc.Col(topCard2, width=2),
            dbc.Col(topCard3, width=2)
        ],
        justify="center"
    ),
    html.Br(style={"marginTop": "2vh"}),

    dbc.Row(
        general_filters
    ),

    html.Br(style={"marginTop": "2vh"}),
    dbc.Row(
        [
            dbc.Col(
                articlesDateOverview,
                width="auto"
            ),
            dbc.Col(
                [categoryRepartition, html.H5(id="test"), dateGraphKPI],
                width="auto"
            ),
        ],
        justify="between"
    ),

    html.Button(id="test_retrieve", children="Pubmed Retrieve")
])


@callback(Output("test_retrieve", "n_clicks"),
          Input("test_retrieve", "n_clicks"))
def RetrieveData(click):
    if click:
        group = PubmedGroup(pathologies=["goiter"], filters=["humans"], threadingObject=5, delay=0.8)
        group.StartRetrieve()
        group.JoinAndCleanDataframe()
    return None
