import dash
from dash import Input, Output, callback
from plotly.subplots import make_subplots

from pages.utilities.dashboard.components import *
from pages.utilities.dashboard.graphParameters import *

'''
This file group all callbacks used in the Dashboard page, they are organized around
their principal component.

You can find the following group of callback:
    - Category selection
    - All simple statistics (you can find bellow the animated banner)
    - Tab with pie chart to analyse category and sub-category repartition
    - Bar chart to analyse studies repartition from different sources
    - Tab with multiple chart to analyse studies by date  
    - Studies dataframe & modal
'''


"""
Category selection
"""

@callback(Output("selected-card", "data"),
          Input("reset", "n_clicks"),
          [Input(f"button-{category.loc[x]['category']}", "n_clicks") for x in category.index])
def StoredDataUpdate(data, *args):
    trigger_button = [p['prop_id'] for p in dash.callback_context.triggered][0]

    try:
        trigger_button = trigger_button.split("-")[1].split(".")[0]

        if trigger_button in all_category:
            return trigger_button
        else:
            return data
    except IndexError:
        if trigger_button == "reset.n_clicks":
            return None
        else:
            return data


"""
CardStatUpdate():
    This callback is used to update the evolution rate of studies by year.
    The first two Input are the year selection and the third is the selected category
    The first output return an icon (aesthetic), the second return the evolution in percentage
    and the third return the evolution in number
    
CardStat2Update():
    This callback is used to update the studies repartition by sponsors class.
    The first Input is the sponsors class selection and the second is the selected category.
    Output are the same as the function above.
    
ResetLightStats():
    This one is used to reinitialize CardStatUpdate() input when the "reset" button is pressed
"""


@callback(Output("card1Output1", "children"),
          Output("card1Output2", "children"),
          Output("card1Output3", "children"),
          Input("card1Input1", "value"),
          Input("card1Input2", "value"),
          Input("selected-card", "data"),
          )
def CardStatUpdate(firstYear, secondYear, data):
    if data is None:
        df = s_base[["nct_id", "study_first_submitted_date"]].copy()
    else:
        df = s_base[s_base["category"] == data][["nct_id", "study_first_submitted_date"]].copy()

    now = datetime.now()
    decision = firstYear == datetime.now().year or secondYear == datetime.now().year

    actualYear = df[(df["study_first_submitted_date"] >= datetime(firstYear, 1, 1)) & (
            df["study_first_submitted_date"] <= datetime(firstYear, now.month if decision else 12,
                                                         now.day if decision else 30))].shape[0]
    pastYear = df[(df["study_first_submitted_date"] >= datetime(secondYear, 1, 1)) & (
            df["study_first_submitted_date"] <= datetime(secondYear, now.month if decision else 12,
                                                         now.day if decision else 30))].shape[0]

    variation = round(((actualYear - pastYear) / pastYear) * 100, 2)
    diff = actualYear - pastYear
    if variation > 0:
        return html.Div(className="bi bi-chevron-up",
                        style={
                            "fontSize": "1.2vmax",
                            "color": "#2CEC47"
                        }), \
               html.H3(f"{variation}%",
                       style={
                           "color": "#2CEC47"
                       }), \
               html.Plaintext(f"+{diff} études",
                              style={
                                  "color": "#2CEC47"
                              }),
    elif variation < 0:
        return html.Div(className="bi bi-chevron-down",
                        style={
                            "fontSize": "1.2vmax",
                            "color": "#F50C0C"
                        }), \
               html.H3(f"{variation}%",
                       id="card1Output2",
                       style={
                           "color": "#F50C0C"
                       }), \
               html.Plaintext(f"{diff} études",
                              style={
                                  "color": "#F50C0C"
                              }),
    else:
        return html.Div(className="bi bi-dash-lg",
                        style={
                            "fontSize": 20,
                        }), \
               html.H3(f"{variation}%",
                       id="card1Output2",
                       style={
                           "color": "black"
                       }), \
               html.Plaintext(f"--"),


@callback(Output("card2Output1", "children"),
          Output("card2Output2", "children"),
          Output("card2Output3", "children"),
          Input("card2Input1", "value"),
          Input("selected-card", "data"))
def CardStat2Update(sp_class, data):
    if data in all_category:
        df = s_base[s_base["category"] == data]
    else:
        df = s_base[["nct_id", "category"]]

    sp = sponsors[sponsors["nct_id"].isin(df.nct_id)]
    studiesCount = sp[sp["new_class"] == sp_class].shape[0]
    repartition = round((studiesCount / sp.shape[0]) * 100, 2)

    if sp_class == "University":
        icon = "bi bi-mortarboard"
    elif sp_class == "Health care Institution":
        icon = "bi bi-hospital"
    elif sp_class == "Industry":
        icon = "bi bi-building"
    elif sp_class == "Government Agency":
        icon = "bi bi-bank"
    elif sp_class == "Other":
        icon = "bi bi-people"
    else:
        icon = None

    return \
        html.Div(className=icon,
                 style={
                     "fontSize": "1.2vmax",
                 }), \
        html.H3(f"{repartition}%"), \
        html.Plaintext(f"{studiesCount} études"),


@callback(Output("card1Input1", "value"),
          Output("card1Input2", "value"),
          Input("reset", "n_clicks"))
def ResetLightStats(reset):
    return 2022, 2021


"""
RepartitionPieUpdate():
    This callback is used to update the pie chart from the "category repartition" tab.
    The first Input is the selected category and all others are the parameters from the "parameters" tab.
    The Output is the pie chart
    
PieByStudiesTypeUpdate():
    Same operation as above but split in 3 pie charts
    
TextUpdate():
    This one is used to update tabs title of pie charts
    
HighlightPieTabs():
    Used to highlight pie tabs
    
ParametersTabUpdating():
    Reinitialize pie charts parameters when the global reset button or the category repartition reset button
    is pressed.
"""

@callback(Output("subCategoryProportion", "figure"),
          Input("selected-card", "data"),
          Input("CRP_studiesType", "value"),
          Input("CRP_studiesStatus", "value"),
          Input("CRP_minAge", "value"),
          Input("CRP_maxAge", "value"),
          )
def RepartitionPieUpdate(data, s_type, s_status, minAge, maxAge, *args):
    df = GetSubCategoryProportion(data, s_type, s_status, minAge, maxAge)
    fig = go.Figure(data=[go.Pie(
        labels=df["view"],
        values=df["nct_id"],
        marker=dict(
            colors=df["color"]
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
        margin=dict(l=0, r=0, t=25, b=0),
        showlegend=True,
        legend=dict(
            x=1.1,
            itemclick=False,
            # orientation="v",
            # font=dict(
            #     size=8
            # )
        )
    )
    return fig


@callback(Output("subCategoryProportionByStudiesType", "figure"),
          Input("selected-card", "data"),
          Input("CRP_studiesStatus", "value"),
          Input("CRP_minAge", "value"),
          Input("CRP_maxAge", "value"),
          )
def PieByStudiesTypeUpdate(data, s_status, minAge, maxAge, *args):
    fig = make_subplots(rows=1, cols=3, specs=[[{"type": "domain"},
                                                {"type": "domain"},
                                                {"type": "domain"}]])

    col = 1
    for i in s_base.study_type.sort_values().unique():
        df = GetSubCategoryProportion(data, i, s_status, minAge, maxAge)

        fig.add_trace(
            go.Pie(
                labels=df["view"],
                values=df["nct_id"],
                title=i,
                marker=dict(
                    colors=df["color"]
                )
            ),
            1, col)

        col += 1

    fig.update_traces(hole=.4,
                      hoverinfo="label+percent")

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
        margin=dict(l=0, r=0, t=25, b=0),
        showlegend=True,
        legend=dict(
            x=1.1,
            itemclick=False,
            # orientation="v",
            # font=dict(
            #     size=8
            # )
        )
    )
    return fig


@callback(Output("title", "children"),
          Output("pieTab1", "label"),
          Output("pieTab2", "label"),
          Input("selected-card", "data"), )
def TextUpdate(data):
    if data in all_category:
        return data, "Sub-category repartition", "Sub-category repartition by studies type"
    else:
        return "Overview", "Category repartition", "Category repartition by studies type"


@callback(Output("CRP_card", "class_name"),
          Output("CRP_card", "style"),
          Input("CRP_highlight", "value"))
def HighlightPieTabs(highlight):
    if highlight:
        return "card mb-4 border-3", {"backgroundColor": "hsl(247.74, 52.54%, 98.43%)",
                                      "borderRadius": "15px",
                                      "borderColor": "#F8DF09"}
    else:
        return "card mb-4 border-1", {"backgroundColor": "hsl(247.74, 52.54%, 98.43%)",
                                      "borderRadius": "15px"}


@callback(Output("parametersItem1", "children"),
          Input("reset", "n_clicks"),
          Input("CRP_reset", "n_clicks"))
def ParametersTabUpdating(*args):
    if args[0] or args[1]:
        return parametersItem1
    else:
        return parametersItem1


"""
BarChartUpdate():
    This callback is used to update the bar chart using parameters from the "parameters" tab.
HighlightBarPlot():
    Used to highlight bar plot when the box is checked.
ParametersTabUpdating():
    Same than callback above but for the bar plot parameters.
"""

@callback(Output("studyTypeBar", "figure"),
          Input("selected-card", "data"),
          Input("SR_dropdown", "value"),
          Input("SR_radioItems", "value"))
def BarChartUpdate(data, selection, divide):
    if data in all_category:
        df = GetCategoryPercent(columns=[selection],
                                groupby=["category", selection],
                                sortby=["category", "nct_id"],
                                sortasc=False,
                                categoryfilter=data,
                                divide=divide,
                                divide_col=selection,
                                drop_duplicates=["nct_id"])
    else:
        df = GetCategoryPercent(columns=[selection],
                                groupby=[selection],
                                sortby=["category", "nct_id"],
                                sortasc=False,
                                divide=divide,
                                divide_col=selection,
                                drop_duplicates=["nct_id"])
        df["category"] = "All"

    s_type = [x for x in df[selection]]
    marker_color = ["#072770", "#031438", "#051d54", "#08318c", "#0a3ba8", "#2866F2", "#4f82f4", "#769ef7", "#9db9f9",
                    "#c4d5fb", "#ebf1fe"]

    fig = go.Figure(data=[
        go.Bar(name="Interventional",
               x=df[df[selection] == y]["category"],
               y=df[df[selection] == y]["nct_id"],
               text=f"{df[df[selection] == y][selection].iloc[0]}<br>{df[df[selection] == y]['percent'].iloc[0]}",
               insidetextanchor="middle",
               marker=dict(color=marker_color[-x],
                           line=dict(width=2, color="white")),
               )
        for x, y in enumerate(s_type)])

    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            constrain="domain"
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        barmode='stack',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=30),
        showlegend=False,
    )

    return fig


@callback(Output("SR_card", "class_name"),
          Output("SR_card", "style"),
          Input("SR_highlight", "value"))
def HighlightBarPlot(highlight):
    if highlight:
        return "card mb-4 border-3", {"backgroundColor": "hsl(247.74, 52.54%, 98.43%)",
                                      "borderRadius": "15px",
                                      "borderColor": "#F8DF09"}
    else:
        return "card mb-4 border-1", {"backgroundColor": "hsl(247.74, 52.54%, 98.43%)",
                                      "borderRadius": "15px"}


@callback(Output("parametersItem3", "children"),
          Input("reset", "n_clicks"),
          Input("SR_reset", "n_clicks"))
def ParametersTabUpdating(*args):
    if args[0] or args[1]:
        return parametersItem3
    else:
        return parametersItem3


"""
FigureHistoricalUpdate():
    Same than BarChartUpdate() callback but for the graph from the "historical date overview" tab.
ParametersTabUpdating():
    Same than function above but for the plot chart parameters.
"""


@callback(Output("studiesDateEventByYear", "figure"),
          Input("selected-card", "data"),
          Input("SDO_checklist", "value"),
          Input("SDO_minYear", "value"),
          Input("SDO_maxYear", "value"),
          Input("SDO_monthDisplay", "value"),
          Input("SDO_radioItems", "value"))
def FigureHistoricalUpdate(data, dateColumn, minYear, maxYear, periodDisplay, figure):
    dateColumn = dateColumn if isinstance(dateColumn, list) else []
    fig = go.Figure(data=StudiesByYear(data, dateColumn, minYear, maxYear, periodDisplay, figure))

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
        margin=dict(l=0, r=0, t=25, b=0),
        showlegend=True,
    )
    return fig


@callback(Output("parametersItem2", "children"),
          Input("reset", "n_clicks"),
          Input("SDO_reset", "n_clicks"))
def ParametersTabUpdating(*args):
    if args[0] or args[1]:
        return parametersItem2
    else:
        return parametersItem2


"""
SelectedStudy():
    Store the row index in a dcc.Store component.
OpenStudiesModal():
    Open a modal (new window) when the "more informations" button is pressed, if no
    study selected the modal can't be open.
"""

@callback(Output("studyIndex", "data"),
          Input("datatable", "selected_rows"))
def SelectedStudy(row):
    return row


@callback(Output("studiesModal", "children"),
          Output("moreStudyInfo", "n_clicks"),
          Input("studyIndex", "data"),
          Input("moreStudyInfo", "n_clicks"))
def OpenStudiesModal(data, n_clicks):
    if n_clicks:
        return ModalStudiesInfo(data if data is not None else [0], True), None
    else:
        return None, None
