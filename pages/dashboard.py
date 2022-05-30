import dash
from dash import Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots

from pages.utilities.helpers import *
from pages.utilities.const import *
from pages.utilities.dashboardComponents import *
from pages.utilities.dashboardParameters import *

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
                                                        lightStatistic2
                                                    ]
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(
                                                                    tabWithMultipleCharts,
                                                                    style={
                                                                        "display": "flex",
                                                                        "alignItems": "center",
                                                                        "justifyContent": "right",
                                                                        "horizontalAlign": "center",
                                                                    },
                                                                    width="auto"
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
                                                                    width=True
                                                                )
                                                            ]
                                                        ),
                                                    ],
                                                ),
                                                dbc.Col(
                                                    barPlotByStudiesType,
                                                    width="auto",
                                                ),
                                            ]
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


@callback(Output("SDO_card", "class_name"),
          Output("SDO_card", "style"),
          Input("SDO_highlight", "value"))
def HighlightPieTabs(highlight):
    if highlight:
        return "card mb-4 border-3", {"backgroundColor": "hsl(247.74, 52.54%, 98.43%)",
                                      "borderRadius": "15px",
                                      "borderColor": "#F8DF09"}
    else:
        return "card mb-4 border-1", {"backgroundColor": "hsl(247.74, 52.54%, 98.43%)",
                                      "borderRadius": "15px"}


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

@callback(Output("investigators_datatable", "children"),
          Input("selected-card", "data"))
def SponsorsDatatableUpdating(data):
    df = s_base[s_base["category"] == data] if data in all_category else s_base
    inv = investigators[investigators["nct_id"].isin(df.nct_id)]

    # count = inv[["name", "nct_id"]].groupby("name").count().reset_index()

    table = \
        dash_table.DataTable(
            id="datatable",
            data=inv.to_dict('records'),
            columns=[{"name": i, "id": i} for i in
                     inv[["name", "city", "state",
                          "zip", "country", "continent"]].columns],
            page_size=10,
            filter_action="native",
            sort_action="native",
            style_table={'overflowX': 'auto'},
            style_cell={
                'height': 'auto',
                # all three widths are needed
                'minWidth': '180px', 'width': '180px', 'maxWidth': '200px',
                'whiteSpace': 'normal'
            },
            style_header={
                'backgroundColor': "#0D6986",
                "color": "white",
                "fontWeight": 900,
                "fontSize": "12px"
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(223, 226, 232)',
                    'color': 'black'
                },
                {
                    'if': {'row_index': 'even'},
                    'backgroundColor': 'rgb(245, 249, 255)'
                }
            ]
        )

    return table


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


"""
########################################################################################################################
THIS CALLBACK UPDATE STORE COMPONENT USED TO DEFINE
IF A CATEGORY HAS BEEN SELECTED OR NOT
OR IF THE RESET BUTTON IS SELECTED
########################################################################################################################
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
########################################################################################################################
THIS CALLBACK IS USED TO UPDATES ALL TEXT COMPONENT 
########################################################################################################################
"""


@callback(Output("title", "children"),
          Output("pieTab1", "label"),
          Output("pieTab2", "label"),
          Input("selected-card", "data"), )
def TextUpdate(data):
    if data in all_category:
        return data, "Sub-category repartition", "Sub-category repartition by studies type"
    else:
        return "Overview", "Category repartition", "Category repartition by studies type"


"""
########################################################################################################################

########################################################################################################################
"""


@callback(Output("card1Input1", "value"),
          Output("card1Input2", "value"),
          Input("reset", "n_clicks"))
def ResetLightStats(reset):
    return 2022, 2021


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
                            "fontSize": 20,
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
                            "fontSize": 20,
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
                     "fontSize": 20,
                 }), \
        html.H3(f"{repartition}%"), \
        html.Plaintext(f"{studiesCount} études"),


"""
########################################################################################################################
THIS CALLBACK IS USED TO UPDATE THE VERTICAL BAR CHART BY STUDY_TYPE
########################################################################################################################
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
                                divide_col=selection)
    else:
        df = GetCategoryPercent(columns=[selection],
                                groupby=[selection],
                                sortby=["category", "nct_id"],
                                sortasc=False,
                                divide=divide,
                                divide_col=selection)
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
        height=800,
        width=150,
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


"""
########################################################################################################################
THIS CALLBACK IS USED TO UPDATE THE PIE CHART FROM THE "NO FILTER" TAB
########################################################################################################################
"""


@callback(Output("subCategoryProportion", "figure"),
          Input("selected-card", "data"),
          Input("CRP_studiesType", "value"),
          Input("CRP_studiesStatus", "value"),
          Input("CRP_minAge", "value"),
          Input("CRP_maxAge", "value"),
          )
def pieNoFilterUpdate(data, s_type, s_status, minAge, maxAge, *args):
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
        height=290,
        width=900,
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


"""
########################################################################################################################
THIS CALLBACK IS USED TO UPDATES PIES CHARTS FROM THE "BY STUDIES TYPE" TAB
########################################################################################################################
"""


@callback(Output("subCategoryProportionByStudiesType", "figure"),
          Input("selected-card", "data"),
          Input("CRP_studiesStatus", "value"),
          Input("CRP_minAge", "value"),
          Input("CRP_maxAge", "value"),
          )
def pieByStudiesTypeUpdate(data, s_status, minAge, maxAge, *args):
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
        height=290,
        width=900,
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


"""
########################################################################################################################
THIS CALLBACK IS USED TO UPDATE THE LINE CHART WITH NEW AND COMPLETED STUDIES
########################################################################################################################
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
        height=350,
        width=950,
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


@callback(Output("parametersItem1", "children"),
          Input("reset", "n_clicks"),
          Input("CRP_reset", "n_clicks"))
def ParametersTabUpdating(*args):
    if args[0] or args[1]:
        return parametersItem1
    else:
        return parametersItem1


@callback(Output("parametersItem2", "children"),
          Input("reset", "n_clicks"),
          Input("SDO_reset", "n_clicks"))
def ParametersTabUpdating(*args):
    if args[0] or args[1]:
        return parametersItem2
    else:
        return parametersItem2


@callback(Output("parametersItem3", "children"),
          Input("reset", "n_clicks"),
          Input("SR_reset", "n_clicks"))
def ParametersTabUpdating(*args):
    if args[0] or args[1]:
        return parametersItem3
    else:
        return parametersItem3
