from pages.utilities.pubmed_dashboard.components import *
from pages.utilities.pubmed_const import *
import plotly.graph_objects as go
import math

@callback(Output("categoryRepartition", "figure"),
          Input("categoryRepartition", "figure"),
          Input("publication_type", "value"),
          Input("population", "value"))
def DisplayCategoryRepartitionChart(figure, p_type, pop):
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
          Input("articleDateOverview", "figure"),
          Input("publication_type", "value"),
          Input("population", "value"),
          Input("dateCategory", "value"),
          Input("dateFrequency", "value"),
          Input("datePickerRange", "start_date"),
          Input("datePickerRange", "end_date"),
          Input("date_checklist", "value"))
def DisplayArticlesDateOverview(figure, p_type, pop, cond, freq, startDate, endDate, checklist):

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


@callback(Output("dateCategory", "value"),
          Input("selectAllCategory", "value"),
          Input("dateCategory", "options"),
          Input("dateCategory", "value"))
def SelectAllCategory(check, dropdown_options, actual_value):
    if check is not None and len(check) == 1:
        return dropdown_options
    else:
        return actual_value

