import dash
from dash import dcc, Input, Output, State, callback, html
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
                                            topAnimatedBanner
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
                                                        dbc.Row(
                                                            [
                                                                html.Plaintext("Age range",
                                                                               style={
                                                                                   "fontSize": "15px"
                                                                               })
                                                            ],
                                                            justify="center", align="center",
                                                            style={
                                                                "textAlign": "center"
                                                            }
                                                        ),
                                                        dbc.Row(
                                                            [
                                                                dcc.RangeSlider(min=0,
                                                                                max=100,
                                                                                step=5,
                                                                                value=[0, 100],
                                                                                id="age_range_slider")
                                                            ]
                                                        ),
                                                        html.Br(),
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(
                                                                    [
                                                                        dcc.Graph(
                                                                            id="studiesDateEventByYear",
                                                                            config={
                                                                                'displayModeBar': False,
                                                                            },
                                                                        )
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
                                        )
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
                dcc.Store(id="selected-card"),
                dcc.Store(id="dataSliderButton",
                          data=False)
            ],
        )
    ],
    style={
        # "overflow": "scroll"
    }
)

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
          Output("Pietab1", "label"),
          Output("Pietab2", "label"),
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
                                divisionby="selection",
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
          Input("age_range_slider", "value"),
          State("CRP_studiesType", "value"),
          State("CRP_studiesStatus", "value"),
          Input("boolCategoryRepartition", "on"))
def pieNoFilterUpdate(data, age_range, s_type, s_status, *args):
    age_range = list((map(lambda x: int(float(x)), age_range)))
    df = GetSubCategoryProportion(data, s_type, s_status, age_range)
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
        margin=dict(l=0, r=0, t=0, b=0),
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
          State("CRP_studiesStatus", "value"),
          State("age_range_slider", "value"),
          Input("boolCategoryRepartition", "on"))
def pieByStudiesTypeUpdate(data, s_status, age_range, *args):
    fig = make_subplots(rows=1, cols=3, specs=[[{"type": "domain"},
                                                {"type": "domain"},
                                                {"type": "domain"}]])

    col = 1
    for i in s_base.study_type.sort_values().unique():
        df = GetSubCategoryProportion(data, i, s_status, age_range)

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
        margin=dict(l=0, r=0, t=0, b=0),
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
          Input("selected-card", "data"))
def LinePlotByYearUpdate(data):
    fig = go.Figure(data=StudiesByYear(data))

    fig.update_layout(
        height=250,
        width=950,
        title={
            'text': 'New and completed studies by year',
            'y': 0.9,
            'x': 0.5,
            "xanchor": "center",
            "yanchor": "top"
        },
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=True,
            color='black',
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


@callback(Output("test", "children"),
          Output("testt", "children"),
          Input("boolCategoryRepartition", "on"),
          Input("boolBarStudiesType", "on"))
def ParametersTabUpdating(*args):
    return categoryRepartitionPie if args[0] else default, \
           "True2" if args[1] else None


# @callback(Output("category_button", "data"),
#           Input("category_button", "data"),
#           Input("reset", "n_clicks"),
#           [[Input(f"title-{category.loc[x]['category']}", "children"),
#             Input(f"button-{category.loc[x]['category']}", "n_clicks")] for x in category.index],
#           )
# def VisualizationDataUpdate(data, range, *args):
#     category_selected = [p['prop_id'] for p in dash.callback_context.triggered][0]
#
#     data = None if category_selected == "reset.n_clicks" else data
#
#     category_selected = "." if category_selected in ["reset.n_clicks", "age_range_slider.value"] else category_selected
#
#     data = category_selected if category_selected != "." else data
#
#     color_pie = ["hsl(185.23, 100%, 52.75%)",
#                  "hsl(201.22, 95.82%, 53.14%)",
#                  "hsl(216.05, 100%, 55.29%)",
#                  "hsl(230.67, 98.25%, 55.1%)",
#                  "hsl(243.98, 100%, 55.69%)",
#                  "hsl(244.41, 100%, 86.67%)",
#                  "hsl(258.18, 78.2%, 58.63%)",
#                  "hsl(258, 77.78%, 35.29%)"]
#
#     news_and_completed_study_by_year = go.Figure(data=StudiesByYear(category_selected))
#
#     news_and_completed_study_by_year.update_layout(
#         height=250,
#         width=950,
#         title={
#             'text': 'New and completed studies by year',
#             'y': 0.9,
#             'x': 0.5,
#             "xanchor": "center",
#             "yanchor": "top"
#         },
#         xaxis=dict(
#             showgrid=False,
#             showline=False,
#             showticklabels=True,
#             color='black',
#             zeroline=False,
#         ),
#         yaxis=dict(
#             showgrid=False,
#             showline=False,
#             showticklabels=False,
#             zeroline=False,
#         ),
#         paper_bgcolor='rgba(0, 0, 0, 0)',
#         plot_bgcolor='rgba(0, 0, 0, 0)',
#         margin=dict(l=0, r=0, t=0, b=0),
#         showlegend=False,
#     )
#
#     return data
