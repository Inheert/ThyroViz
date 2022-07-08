import dash
import dash_labs as dl
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State, callback
from datetime import datetime
import os
import glob

interval = 10

FONT_AWESOME = "https://use.fontawesome.com/releases/v5.7.2/css/all.css"
clinical_trials_pages = ["pages.clinical_trials.dashboard", "pages.clinical_trials.investigators", "pages.clinical_trials.sponsors", "pages.clinical_trials.studies"]
pubmed_pages = ["pages.pubmed.dashboard"]

app = dash.Dash(__name__, plugins=[dl.plugins.pages], external_stylesheets=[dbc.themes.BOOTSTRAP,
                                                                            dbc.icons.BOOTSTRAP,
                                                                            FONT_AWESOME],
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1"}
                ], suppress_callback_exceptions=True)

server = app.server

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
    "backgroundColor": "rgba(0,0,0,0)",
    "backgroundPosition": "right top"
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "marginLeft": "0rem",
    "marginRight": "2rem",
    "padding": "2rem 1rem"
}

sidebar = \
    html.Div(
        [
            dbc.Button(">", id="slideMenuButton", style={"position": "fixed"}),
            dbc.Offcanvas(
                id="slideMenu",
                is_open=False,
                style={
                    "width": "22rem",
                    "backgroundColor": "#f8f9fa",
                },
                children=[
                    html.Div(
                        [

                            # Div de la sidebar comprennant les éléments suivants :
                            #     - Titre
                            #     - tiret de séparation
                            #     - les différentes pages (trouvable dans le dossier page du projet)

                            html.Div(
                                [
                                    html.H2("ThyroResearch", className="display-6"),
                                    html.Hr(),
                                    html.P(
                                        "Navigate through the different tools of ThyroResearch", className="lead"
                                    ),
                                    html.Br(),

                                    html.P("Clinical Trials",
                                           style={
                                               "fontWeight": 800,
                                               "color": '#096BFE'
                                           }),
                                    html.Hr(),
                                    dbc.Nav(
                                        [
                                            dbc.NavLink(page["name"], href=page["path"], active="exact")
                                            for page in dash.page_registry.values()
                                            if page["module"] in clinical_trials_pages
                                        ],
                                        vertical=True,
                                        pills=True,
                                    ),
                                    html.Br(),

                                    html.P("Pubmed",
                                           style={"fontWeight": 800,
                                                  "color": "#096BFE"}),
                                    html.Hr(),
                                    dbc.Nav(
                                        [
                                            dbc.NavLink(page["name"], href=page["path"], active="exact")
                                            for page in dash.page_registry.values()
                                            if page["module"] in pubmed_pages
                                        ],
                                        vertical=True,
                                        pills=True,
                                    ),

                                ],
                                style={
                                    "height": "87%"
                                }
                            ),
                            html.Plaintext("Last update:"),
                            html.Plaintext(
                                f"{datetime.fromtimestamp(os.path.getmtime(glob.glob(f'{os.path.abspath(os.curdir)}/script/clinical_trials/sql/visualisation/CSV_files/studies.csv')[0])).strftime('%Y-%m-%d %H:%M')}",
                                id="lastUpdate",
                                style={
                                    "marginTop": "-15px"
                                }),

                            # Layout comprennant les éléments suivants :
                            #     - texte "dernière mise à jour"
                            #     - date de dernière mise à jour
                            #     - bouton mise à jour
                            #     - loading component
                            #     - timer
                            #     - boite de dialogue

                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.Button("Update",
                                                       id="updateButton",
                                                       disabled=True)

                                        ],
                                        width="auto"
                                    ),
                                    dbc.Col(
                                        [
                                            dcc.Loading(
                                                id="loading-1",
                                                type="default",
                                                children=html.Div(id="updateLoading"),
                                                style={
                                                    "marginTop": "41%"
                                                }
                                            ),
                                            dcc.Interval(interval=interval * 100, id="timerRefreshButton"),
                                            dcc.ConfirmDialog(
                                                id='confirm-update',
                                                message='Voulez-vous mettre les données à jour ?',
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

                            #     style={
                            #         "backgroundColor": "black",
                            #         "display": "flex",
                            #         "alignItems": "flex-end",
                            #
                            #     }
                            # )

                        ],
                        style=SIDEBAR_STYLE,
                    )
                ]
            ),
            dcc.Store(id="default_page", data=False)
        ]
    )

content = html.Div(dl.plugins.page_container, style=CONTENT_STYLE, id="page-content")
# app.layout = html.Div([dcc.Location(id="url"), sidebar, content])
app.layout = html.Div(
    dbc.Row(
        [
            dcc.Location(id="url"),
            dbc.Col(sidebar, width="auto"),
            dbc.Col(content),
            dcc.Store(id="test")
        ]
    ),
)


@callback(Output('slideMenu', 'is_open'),
          Input('slideMenuButton', 'n_clicks'),
          [State('slideMenu', 'is_open')]
          )
def ToggleSlideMenu(n1, is_open):
    if n1:
        return not is_open
    return is_open

# Callback réagissant au clique du bouton de mise à jour afin d'afficher une notif d'avertissement pour le lancement
# de la mise à jour des données
# Le callback possède également un timer afin de vérifier tout les x temps la disponibilité du bouton mise à jour
# afin d'éviter le spam du bouton est un crash dans l'algo de récupération

@callback([Output("confirm-update", "displayed"),
           Output("updateButton", "disabled"),
           Output("updateButton", "n_clicks")],
          Input("timerRefreshButton", "n_intervals"),
          Input("updateButton", "n_clicks"))
def confirmButton(timer, button):
    from script.clinical_trials.ct_const import loading
    if button:
        return True, True, None

    if timer and not loading:
        try:
            buttonDisable = False if datetime.now().timestamp() - datetime.fromtimestamp(
                os.path.getmtime(glob.glob(
                    f'{os.path.abspath(os.curdir)}/script/clinical_trials/sql/visualisation/CSV_files/studies.csv')[
                                     0])).timestamp() > 100 else True
        except FileNotFoundError:
            buttonDisable = True
        if not buttonDisable:
            return False, False, None
        else:
            return False, True, None

    return False, True, None


# Callback lançant la récupération des données après le message de confirmation.
# Un "loading" se lance alors le temps de la récupération.
# Une fois la mise à jour terminé la date de dernière mise à jour s'actualise.

@callback(Output("updateLoading", "children"),
          Output("lastUpdate", "children"),
          Input("confirm-update", "submit_n_clicks"))
def updatingData(submit_n_clicks):
    lastUpdate = f"{datetime.fromtimestamp(os.path.getmtime(glob.glob(f'{os.path.abspath(os.curdir)}/script/clinical_trials/sql/visualisation/CSV_files/studies.csv')[0])).strftime('%Y-%m-%d %H:%M')}"

    if submit_n_clicks:
        from script.clinical_trials.ct_core import appLaunch
        appLaunch()
        return None, lastUpdate
    return None, lastUpdate

# @callback(Output("page-content", "children"),
#           Input("page-content", "children"))
# def Avoid404Page(children: dict):
#     href = children["props"]["children"][0]["props"]["href"]
#
#     if href == "http://127.0.0.1:8050/":
#         children["props"]["children"][0]["props"]["href"] = "http://127.0.0.1:8050/clinical-trials/dashboard"
#         return children
#     else:
#         return children

if __name__ == "__main__":
    app.run_server(debug=True)
