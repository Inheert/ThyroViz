import dash
from dash import html, Input, Output, callback
from script.pubmed.PubmedGroup import *

dash.register_page(__name__)

layout = html.Div([
    html.Button(id="test_retrieve", children="Pubmed Retrieve")
])


@callback(Output("test_retrieve", "n_clicks"),
          Input("test_retrieve", "n_clicks"))
def RetrieveData(click):
    if click:
        group = PubmedGroup(pathologies=["goitre"], filters=["humans"], threadingObject=5, delay=0.8)
        group.StartRetrieve()
        group.JoinAndCleanDataframe()
    return None
