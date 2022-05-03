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
                            topCard1,
                            width=True
                        ),
                        dbc.Col(
                            topCard2,
                            width=True
                        ),
                        dbc.Col(
                            topCard3,
                            width=True
                        ),
                        dbc.Col(
                            topCard4,
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
                                                    barPlotByStudiesType,
                                                    width="auto"
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
                                                                        "justifyContent": "center",
                                                                        "horizontalAlign": "center",
                                                                    },
                                                                    width=True
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
                                                                        "justifyContent": "center",
                                                                        "horizontalAlign": "center",
                                                                    },
                                                                    width=True
                                                                )
                                                            ]
                                                        ),
                                                    ],
                                                ),
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col([
                                                    dcc.Dropdown(options=[
                                                        x for x in s_base.category.unique()
                                                    ],
                                                        value="Thyroid neoplasms",
                                                        clearable=False
                                                    ),
                                                    dcc.Dropdown(options=[
                                                        x for x in s_base.sub_category.unique()
                                                    ],
                                                        multi=True,
                                                        style={
                                                            "marginTop": "5px"
                                                        })
                                                ],
                                                    style={
                                                        "maxWidth": "400px"
                                                    }
                                                ),
                                                dbc.Col([
                                                    html.H5(id="test"),
                                                ],
                                                    style={
                                                        "display": "flex",
                                                        "alignItems": "center",
                                                        "justifyContent": "center",
                                                        "horizontalAlign": "center",
                                                        "marginLeft": "3vh"
                                                    }
                                                )
                                            ],
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
                    [
                        dbc.Col(
                            [
                                dbc.Button(
                                    id="moreStudyInfo",
                                    children="More informations"
                                )
                            ],
                            style={
                                "marginLeft": "27px"
                            }
                        ),
                    ],
                    style={
                        "marginTop": "25px"
                    }
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dash_table.DataTable(
                                    id="datatable",
                                    data=s_base.to_dict('records'),
                                    columns=[{"name": i, "id": i} for i in
                                             s_base[["nct_id", "category", "sub_category", "study_first_submitted_date",
                                                     "primary_completion_date", "completion_date", "study_type",
                                                     "overall_status", "study_phases", "minimum_age_num",
                                                     "maximum_age_num"]].columns],
                                    page_size=15,
                                    filter_action="native",
                                    sort_action="native",
                                    row_selectable="single",
                                    style_data_conditional=[
                                        {
                                            'if': {'row_index': 'odd'},
                                            'backgroundColor': 'gray',
                                            'color': 'white'
                                        }
                                    ]
                                )
                            ],
                            width=True,
                            style={
                                "display": "flex",
                                "alignItems": "center",
                                "justifyContent": "center",
                                "horizontalAlign": "center",
                                "marginLeft": "3vh"
                            }
                        )
                    ],
                    style={
                        "marginTop": "10px"
                    }
                ),

                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Header")),
                        dbc.ModalBody(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dbc.CardGroup(
                                                    [
                                                        dbc.Card(
                                                            dbc.CardBody(
                                                                [
                                                                    html.H4("Nct ID:"),
                                                                    html.H6("NCT465464615648446")
                                                                ]
                                                            ),
                                                            className="mt-4 shadow",
                                                            style={
                                                                "borderRadius": "5px",
                                                                "marginRight": "10px"
                                                            }
                                                        ),
                                                        dbc.Card(
                                                            dbc.CardBody(
                                                                [
                                                                    html.H4("Category:"),
                                                                    html.H6("Thyroid neoplasms")
                                                                ]
                                                            ),
                                                            className="mt-4 shadow",
                                                            style={
                                                                "borderRadius": "5px",
                                                                "marginRight": "10px"
                                                            }
                                                        ),
                                                        dbc.Card(
                                                            dbc.CardBody(
                                                                [
                                                                    html.H4("Sub-category:"),
                                                                    html.H6("Thyroid cancers")
                                                                ]
                                                            ),
                                                            className="mt-4 shadow",
                                                            style={
                                                                "borderRadius": "5px"
                                                            }
                                                        )
                                                    ]
                                                )
                                            ],
                                            style={
                                                "display": "flex",
                                                "alignItems": "center",
                                                "justifyContent": "center",
                                                "horizontalAlign": "center",
                                            }
                                        )
                                    ],
                                    style={
                                        "display": "flex",
                                        "alignItems": "center",
                                        "justifyContent": "center",
                                        "horizontalAlign": "center"
                                    }
                                )
                            ]
                        )
                    ],
                    id="studiesModal",
                    is_open=False,
                    size="xl"
                ),

                dcc.Store(id="selected-card"),
                dcc.Store(id="dataSliderButton",
                          data=False),
                dbc.Row(CRP_default),
                dbc.Row(SDO_default)
            ],
        )
    ],
    style={
        # "overflow": "scroll"
    }
)


@callback(Output("studiesModal", "is_open"),
          Output("moreStudyInfo", "n_clicks"),
          Input("datatable", "selected_rows"),
          Input("moreStudyInfo", "n_clicks"),
          State("studiesModal", "is_open"))
def OpenStudyModal(row, n_clicks, is_open):
    if n_clicks and row:
        return not is_open, None
    return is_open, None


@callback(Output("test", "children"),
          Input("datatable", "selected_rows"))
def test(selected):
    if selected is None:
        return None
    else:
        return s_base.loc[selected]["nct_id"]


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
          Input("selected-card", "data"))
def TextUpdate(data):
    if data in all_category:
        return data, "Sub-category repartition", "Sub-category repartition by studies type"
    else:
        return "Overview", "Category repartition", "Category repartition by studies type"


"""
########################################################################################################################
THIS CALLBACK IS USED TO UPDATE THE VERTICAL BAR CHART BY STUDY_TYPE
########################################################################################################################
"""


@callback(Output("studyTypeBar", "figure"),
          Input("selected-card", "data"))
def BarChartUpdate(data):
    if data in all_category:
        df = GetCategoryPercent(columns=["study_type"],
                                groupby=["category", "study_type"],
                                sortby=["category", "nct_id"],
                                sortasc=False,
                                categoryfilter=data)
    else:
        df = GetCategoryPercent(columns=["study_type"],
                                groupby=["study_type"],
                                sortby=["category", "nct_id"],
                                sortasc=False)
        df["category"] = "All"

    s_type = [x for x in df["study_type"]]
    marker_color = ["#342883", "#4a39bb", "#6f60cf"]

    fig = go.Figure(data=[
        go.Bar(name="Interventional",
               x=df[df["study_type"] == y]["category"],
               y=df[df["study_type"] == y]["nct_id"],
               text=f"{df[df['study_type'] == y]['study_type'].iloc[0]}<br>{df[df['study_type'] == y]['percent'].iloc[0]}",
               insidetextanchor="middle",
               marker=dict(color=marker_color[x],
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
        hovermode=False
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
          Input("boolCategoryRepartition", "on"))
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
          Input("boolCategoryRepartition", "on"))
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


@callback(Output("param1", "children"),
          Input("boolCategoryRepartition", "on"),
          Input("reset", "n_clicks"),
          Input("CRP_reset", "n_clicks"))
def ParametersTabUpdating(*args):
    return categoryRepartitionParameters if args[0] else CRP_default


@callback(Output("param2", "children"),
          Input("SDO_bool", "on"),
          Input("reset", "n_clicks"),
          Input("SDO_reset", "n_clicks")
          )
def ParametersTabUpdating(*args):
    return studiesDateOverviewParameters if args[0] else SDO_default
