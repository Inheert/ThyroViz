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
    html.Br(style={"marginTop": "2vh"}),

    dbc.Row(
        [
            dbc.Col(
                articlesDateOverview,
                width="auto"
            ),
            dbc.Col(
                [categoryRepartition],
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
    dcc.Store(id="dataframe_store"),
    dcc.Download(id="download_dataframe")
])


@callback(Output("observational_type", "disabled"),
          Input("onlyObservational", "value"))
def EnableObservationalDropdown(only_obs: list):
    if len(only_obs) > 0:
        return False
    else:
        return True

@callback(Output("dataframe_store", "data"),
          Input("onlyObservational", "value"),
          Input("dateCategory", "value"),
          Input("dateFrequency", "value"),
          Input("date_checklist", "value"),
          Input("articleDateOverview", "clickData"),
          Input("articles_input", "value"),
          Input("publication_type", "value"),
          Input("population", "value"),
          Input("articles_search_col", "value"))
def UpdateArticlesOverview(only_obs: list, category: list, freq: str, checklist: list, graphClick: dict, txt_input: str,
                           p_type: list, pop: list, colToSearch: list):

    checklist = ["None"] if checklist is None or len(checklist) < 1 else checklist

    df = articles.copy()

    if len(only_obs) > 0:
        df = df[df.PMID.isin(observational.PMID)]

    df["month"] = df["Entrez_date"].apply(lambda x: x.month)
    df["year"] = df["Entrez_date"].apply(lambda x: x.year)

    if len(p_type) > 0:
        df = df[df.PMID.isin(publication_type[publication_type.Publication_type.isin(p_type)]["PMID"])]

    if len(pop) > 0:
        df = df[df.PMID.isin(population[population.Population.isin(pop)]["PMID"])]

    if graphClick:

        if len(category) > 0 and checklist[0] == "Show graph by conditions":
            df = df[df.PMID.isin(
                df_condition[df_condition.Category == category[graphClick["points"][0]["curveNumber"]]]["PMID"])]

        elif len(category) > 0 and checklist[0] == "None":
            df = df[df.PMID.isin(df_condition[df_condition.Category.isin([x for x in category])]["PMID"])]

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
        if len(category) > 0 and checklist[0] == "None":
            df = df[df.PMID.isin(df_condition[df_condition.Category.isin([x for x in category])]["PMID"])]

    if (colToSearch and len(colToSearch) > 0) and (txt_input and len(txt_input) > 1):

        df["Input_found"] = False

        for col in colToSearch:
            print(col)
            df["Input_found"] = df[col].apply(lambda x: True if txt_input.lower().strip() in str(x) else True if x is True else False)

        df = df[df["Input_found"] == True]

        # df_list = []
        # print("pass")
        #
        # for col in colToSearch:
        #     temp_df = df.copy()
        #     temp_df = temp_df[txt_input in temp_df[col]]
        #     df_list.append(temp_df)
        #
        # new_df = pd.DataFrame()
        #
        # for temp_df in df_list:
        #     new_df = pd.concat(new_df, temp_df)
        #
        # df = new_df

    return df.to_dict('records')


@callback(Output("download_dataframe", "data"),
          Output("download_button", "n_clicks"),
          Input("download_button", "n_clicks"),
          Input("dataframe_store", "data"),
          prevent_initial_call=True,)
def DownloadData(n_clicks, df):
    if n_clicks:
        df = pd.DataFrame(df)
        return dcc.send_data_frame(df.to_excel, "data.xlsx", sheet_name="data"), None
    else:
        return None, None

@callback(Output("articles_pagination", "max_value"),
          Input("dataframe_store", "data"))
def PaginationInitializing(df):
    df = pd.DataFrame(df)
    return math.ceil(df.shape[0] / 25)


@callback(Output("accordionArticles", "children"),
          Input("dataframe_store", "data"),
          Input("articles_pagination", "active_page"))
def UpdateAccordionArticles(df, page):
    df = pd.DataFrame(df)
    page = 1 if page is None else page
    page = page - 1
    start_range = 25 * page
    end_range = start_range + 25 if df.shape[0] >= start_range + 25 else df.shape[0]
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
                                    dbc.Col(
                                        [
                                            dbc.Accordion(
                                                [
                                                    dbc.AccordionItem(
                                                        [
                                                            html.P(children=value)
                                                            for value in
                                                            df_condition[df_condition.PMID == df["PMID"].iloc[idx]][
                                                                "Condition"]
                                                        ],
                                                        title="Conditions"
                                                    ),
                                                    dbc.AccordionItem(
                                                        [
                                                            html.P(children=value)
                                                            for value in
                                                            mesh_term[mesh_term.PMID == df["PMID"].iloc[idx]][
                                                                "Mesh_terms"]
                                                        ],
                                                        title="Mesh terms"
                                                    ),
                                                    dbc.AccordionItem(
                                                        [
                                                            html.P(children=value)
                                                            for value in
                                                            other_term[other_term.PMID == df["PMID"].iloc[idx]][
                                                                "Other_terms"]
                                                        ],
                                                        title="Other terms"
                                                    ),
                                                    dbc.AccordionItem(
                                                        [
                                                            html.P(children=value)
                                                            for value in
                                                            population[population.PMID == df["PMID"].iloc[idx]][
                                                                "Population"]
                                                        ],
                                                        title="Population type"
                                                    ),
                                                    dbc.AccordionItem(
                                                        [
                                                            html.P(children=value)
                                                            for value in publication_type[
                                                            publication_type.PMID == df["PMID"].iloc[idx]][
                                                            "Publication_type"]
                                                        ],
                                                        title="Publication type"
                                                    ),
                                                    dbc.AccordionItem(
                                                        [
                                                            html.P(children=value)
                                                            for value in full_author_name[
                                                            full_author_name.PMID == df["PMID"].iloc[idx]][
                                                            "Full_author_name"]
                                                        ],
                                                        title="Authors name"
                                                    ),
                                                    dbc.AccordionItem(
                                                        [
                                                            html.P(children=value)
                                                            for value in
                                                            chemical[chemical.PMID == df["PMID"].iloc[idx]]["Chemical"]
                                                        ],
                                                        title="Chemicals"
                                                    ),
                                                    dbc.AccordionItem(
                                                        [
                                                            html.P(children=value)
                                                            for value in
                                                            observational[observational.PMID == df["PMID"].iloc[idx]][
                                                                "Observational_study_characteristics"]
                                                        ],
                                                        title="Observational study characteristics"
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                                justify="between"
                            )
                        ],
                        title=f"{df['PMID'].iloc[idx]} - {df['Title'].iloc[idx]}"
                    )
                    for idx in range(start_range, end_range)]
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
        print("fini")
    return None
