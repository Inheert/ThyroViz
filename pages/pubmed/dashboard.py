import datetime

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
    html.Br(),
    dbc.Row(
        [
            dbc.Col(
                [
                    accordionArticles
                ]
            ),
        ]
    ),

    html.Button(id="test_retrieve", children="Pubmed Retrieve"),
    dcc.Store(id="dataframe_store")
])


@callback(Output("dataframe_store", "value"),
          Input("dateCondition", "value"),
          Input("dateFrequency", "value"),
          Input("date_checklist", "value"),
          Input("articleDateOverview", "clickData"))
def UpdateArticlesOverview(condition, freq, checklist, graphClick):
    checklist = ["None"] if checklist is None or len(checklist) < 1 else checklist

    print(graphClick)

    df = articles.copy()
    df["month"] = df["Entrez_date"].apply(lambda x: x.month)
    df["year"] = df["Entrez_date"].apply(lambda x: x.year)

    if graphClick:

        if len(condition) > 0 and checklist[0] == "Show graph by conditions":
            df = df[df.PMID.isin(
                df_condition[df_condition.Category == condition[graphClick["points"][0]["curveNumber"]]]["PMID"])]

        elif len(condition) > 0 and checklist[0] == "None":
            df = df[df.PMID.isin(df_condition[df_condition.Category.isin([x for x in condition])]["PMID"])]

        curve_date = datetime.strptime(graphClick["points"][0]["x"], "%Y-%m-%d")
        if freq == "Year":
            df = df[df.year == curve_date.year]
        elif freq == "Month":
            df = df[(df.year == curve_date.year) & (df.month == curve_date.month)]
        elif freq == "Weekly":
            df = df[(df.Entrez_date >= curve_date - timedelta(days=6)) & (df.Entrez_date <= curve_date)]
        # elif freq == "Day":
        #     df = df[(df.Entrez_date == curve_date)]

    else:
        if len(condition) > 0 and checklist[0] == "None":
            df = df[df.PMID.isin(df_condition[df_condition.Category.isin([x for x in condition])]["PMID"])]

    return df.to_dict('records')


@callback(Output("accordionArticles", "children"),
          Input("dataframe_store", "value"))
def UpdateAccordionArticles(df):
    df = pd.DataFrame(df)
    end_range = 100 if df.shape[0] > 100 else df.shape[0]

    accordion = \
        [
            dbc.Accordion(
                [
                    dbc.AccordionItem(
                        [
                            dbc.Row(
                                [
                                    html.H4(df["Title"].iloc[idx]),
                                    html.Br(style={"marginTop": "1vh"}),
                                    dbc.Col(
                                        [
                                            dcc.Markdown(children=f"__DOI__: {df['DOI'].iloc[idx]}"),
                                            dcc.Markdown(children=f"__PII__: {df['PII'].iloc[idx]}"),
                                            html.Br(),
                                            dcc.Markdown(children=f"__Full journal__: {df['Full_journal'].iloc[idx]}"),
                                            dcc.Markdown(
                                                children=f"__Place of publication__: {df['Place_of_publication'].iloc[idx]}"),
                                            html.Br(),
                                            dcc.Markdown(
                                                children=f"__Publication date__: {df['Entrez_date'].iloc[idx]}"),
                                        ],
                                        width="auto"
                                    ),
                                    dbc.Col(
                                        [
                                            dcc.Markdown(children=f"__Abstract__: {df['Abstract'].iloc[idx]}"),
                                        ],
                                        width=3
                                    ),
                                    dbc.Col(),
                                ]
                            )
                        ],
                        title=f"{df['PMID'].iloc[idx]} - {df['Title'].iloc[idx]}"
                    )
                    for idx in range(0, end_range)]
            )
        ]
    return accordion


@callback(Output("test_retrieve", "n_clicks"),
          Input("test_retrieve", "n_clicks"))
def RetrieveData(click):
    if click:
        group = PubmedGroup(pathologies=["goiter"], filters=["humans"], threadingObject=5, delay=0.8)
        group.StartRetrieve()
        group.JoinAndCleanDataframe()
    return None
