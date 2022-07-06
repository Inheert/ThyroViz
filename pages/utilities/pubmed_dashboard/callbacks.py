from pages.utilities.pubmed_dashboard.components import *
from pages.utilities.pubmed_const import *
from pages.utilities.pubmed_helpers import *
import plotly.graph_objects as go
import math

@callback(Output("categoryRepartition", "figure"),
          Input("publication_type", "value"),
          Input("population", "value"))
def DisplayCategoryRepartitionChart(p_type, pop):
    """


    :param figure:
    :param p_type: corresponds to the dropdown menu with id: 'publication_type' to filter df
    :param pop: corresponds to the dropdown menu with id : 'population' used to filter dataframe
    :return: at the end this callback return the pie chart by condition category
    """

    df = df_condition.copy()
    df = df[["PMID", "Category"]]

    if len(p_type) > 0:
        df = df[df.PMID.isin(publication_type[publication_type.Publication_type.isin(p_type)]["PMID"])]
    if len(pop) > 0:
        df = df[df.PMID.isin(population[population.Population.isin(pop)]["PMID"])]

    df = df.drop_duplicates()
    df = df.groupby("Category").count().sort_values(by="PMID", ascending=False).reset_index()

    colors = ["#096BFE", "#013f9d", "#5D16EC", "#9e73f4", "#C116EC", "#610a77", "#512ED4", "#143A88", "#C31068"]

    fig = go.Figure(data=[go.Pie(
        labels=df["Category"],
        values=df["PMID"],
        marker=dict(
            colors=colors
        )
    )])

    fig.update_traces(hole=.4, hoverinfo="label+percent")

    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showline=False,
            zeroline=False,
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=True,
        legend=dict(
            x=0.9,
            itemclick=False,
            # orientation="v",
            # font=dict(
            #     size=8
            # )
        )
    )
    return fig


@callback(Output("articleDateOverview", "figure"),
          Input("publication_type", "value"),
          Input("population", "value"),
          Input("dateCategory", "value"),
          Input("dateFrequency", "value"),
          Input("datePickerRange", "start_date"),
          Input("datePickerRange", "end_date"),
          Input("date_checklist", "value"))
def DisplayArticlesDateOverview(p_type, pop, cond, freq, startDate, endDate, checklist):
    """

    :param p_type: same utility than above
    :param pop: same utilty than above
    :param cond: use the dropdown menu with id: 'dateCategory' to filter the principal df by category condition (based on Category csv)
    :param freq: used the radio button to select the temporality (year, month, weekly, day) the first letter of this parameter is used in the Grouper method to group the dataframe by frequence/period
    :param startDate: first visible date, from the datePickerRange component with id:datePickerRange
    :param endDate: last visible date, same id than above, we are taking another parameter
    :param checklist: refer to the checkbox "Show graph by condition" to create one curve per selected condition (condition from id: dateCategory)
    :return: return a line plot
    """

    startDate = startDate.split("-")
    startDate = [int(x) for x in startDate]

    endDate = endDate.split("-")
    endDate = [int(x) for x in endDate]

    df = articles.copy()
    dff = df_condition.copy()

    df = df[df.PMID.isin(dff.PMID)]

    if len(p_type) > 0:
        df = df[df.PMID.isin(publication_type[publication_type.Publication_type.isin(p_type)]["PMID"])]
    if len(pop) > 0:
        df = df[df.PMID.isin(population[population.Population.isin(pop)]["PMID"])]

    traces = []
    if checklist and "Show graph by conditions" in checklist:
        for category in cond:

            dff = df[df.PMID.isin(df_condition[df_condition.Category == category]["PMID"])]
            dff = dff.groupby(pd.Grouper(key="Entrez_date", freq=freq[0])).count().reset_index().sort_values(
                by="Entrez_date")
            dff = dff[(dff["Entrez_date"] >= datetime(startDate[0], startDate[1], startDate[2])) &
                      (dff["Entrez_date"] <= datetime(endDate[0], endDate[1], endDate[2]))]

            trace = go.Scatter(x=dff["Entrez_date"],
                               y=dff["PMID"],
                               name=category,
                               mode="lines+text",
                               text=dff["PMID"],
                               hovertext=category,
                               textposition="top center")
            traces.append(trace)

    else:
        if len(cond) > 0:
            df = df[df.PMID.isin(df_condition[df_condition.Category.isin(cond)]["PMID"])]

        df = df.groupby(pd.Grouper(key="Entrez_date", freq=freq[0])).count().reset_index().sort_values(by="Entrez_date")
        df = df[(df["Entrez_date"] >= datetime(startDate[0], startDate[1], startDate[2])) & (df["Entrez_date"] <= datetime(endDate[0], endDate[1], endDate[2]))]
        trace = go.Scatter(x=df["Entrez_date"],
                           y=df["PMID"],
                           name="sum of published articles in a period",
                           mode="lines+text",
                           text=df["PMID"],
                           textposition="top center")
        traces.append(trace)

    fig = go.Figure(data=traces)

    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=True,
            zeroline=False,
        ),
        yaxis=dict(
            showgrid=True,
            showline=True,
            showticklabels=True,
            zeroline=False,
        ),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=True,
    )
    return fig


@callback(Output("dataframe_store", "data"),
          Output("results_number", "children"),
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
    """

    :param only_obs: checkbox used like a bool to keep only observation articles, id: 'onlyObservational'
    :param category: dropdown menu to filter all dataframe by category
    :param freq: here freq is used when point on line plot is clicked, for example if year is selected then we can only see all articles publish during the selected date (if i click on 2012 on graph then i will saw all articles from 2012)
    :param checklist: here checklist is used to know if he have to split a new time the dataframe to keep only articles from the selected category curve
    :param graphClick: this parameter catch every click on clickable data on the line plot, if you click on then 'checklist' and 'freq' parameters will be used
    :param txt_input: this parameter is an input to manually search text into our dataframe columns
    :param p_type: publication type, this parameter have the same utility than the previous callback
    :param pop: population, same than above
    :param colToSearch: refer to checklist used to select in wich column will be searched text from 'txt_input' parameter
    :return: this callback return a dataframe to dict stocked in a dcc.Store component
    """

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
            df["Input_found"] = df[col].apply(lambda x: True if txt_input.lower().strip() in str(x) else True if x is True else False)

        df = df[df["Input_found"] == True]

    shape = SpaceInNumber(df.shape[0])

    return df.to_dict('records'), f"Number of results: __{shape}__"


@callback(Output("observational_type", "disabled"),
          Input("onlyObservational", "value"))
def EnableObservationalDropdown(only_obs: list):
    """

    :param only_obs: checkbox used like a bool, if checked then only show observational articles
    :return: if only_obs is checked then enable dropdown menu to filter by observational characteristics
    """
    if len(only_obs) > 0:
        return False
    else:
        return True


@callback(Output("articles_pagination", "max_value"),
          Input("dataframe_store", "data"))
def PaginationInitializing(df):
    """

    :param df: the dataframe stocked previously
    :return: the max value for the pagination rounded up to the nearest whole number
    """
    df = pd.DataFrame(df)
    return math.ceil(df.shape[0] / 25)


@callback(Output("download_dataframe", "data"),
          Output("download_button", "n_clicks"),
          Input("download_button", "n_clicks"),
          Input("dataframe_store", "data"),
          prevent_initial_call=True,)
def DownloadData(n_clicks, df):
    """

    :param n_clicks: refer to the 'download excel' button if click then read the code
    :param df: dataframe previously stored
    :return: if button is clicked then a download will start with the actual dataframe in Excel format
    """
    if n_clicks:
        df = pd.DataFrame(df)
        return dcc.send_data_frame(df.to_excel, "data.xlsx", sheet_name="data"), None
    else:
        return None, None


@callback(Output("accordionArticles", "children"),
          Input("dataframe_store", "data"),
          Input("articles_pagination", "active_page"))
def UpdateAccordionArticles(df, page):
    """

    :param df: dataframe previously stored
    :param page: get the actual page to update visible articles
    :return: return the new articles for the actual page
    """
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


