import dash
from dash import Input, Output, State, callback, dash_table, html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from plotly.subplots import make_subplots

from pages.utilities.const import *
from pages.utilities.investigatorsComponents import *

dash.register_page(__name__)

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1("Investigators analysis")
                    ]
                ),
            ],
            justify="center", align="center"
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        filterCard,
                    ]
                ),
                dbc.Col(
                    [
                        mapSelection
                    ],
                    width=7
                ),
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        invDatatable,
                    ],
                    width="auto"
                ),
                dbc.Col(
                    [
                        investigatorInfos
                    ]
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        studiesDatatable
                    ]
                ),
                dbc.Col(
                    [
                    ]
                ),
            ]
        ),
        dcc.Store(id="dfStored")
    ]
),


@callback(Output("investigators_map", "figure"),
          Output("filtersInfos", "children"),
          Input("categorySelection", "value"),
          Input("stypeSelection", "value"),
          Input("statusSelection", "value"),
          Input("phasesSelection", "value"))
def GeoInvestigatorsUpdate(category, stype, status, phase):
    inv = investigators.copy()
    df = s_base.copy()

    if category:
        inv = inv[inv["nct_id"].isin(s_base[s_base.category.isin(category)]["nct_id"])]
        df = df[df.category.isin(category)]
    if stype:
        inv = inv[inv["nct_id"].isin(s_base[s_base.study_type.isin(stype)]["nct_id"])]
        df = df[df.study_type.isin(stype)]
    if status:
        inv = inv[inv["nct_id"].isin(s_base[s_base.overall_status.isin(status)]["nct_id"])]
        df = df[df.overall_status.isin(status)]
    if phase:
        df = df[df.study_phases.isin(phase)]
        inv = inv[inv["nct_id"].isin(s_base[s_base.study_phases.isin(phase)]["nct_id"])]

    inv.drop_duplicates(subset=["name", "city", "country"], keep="first", inplace=True)
    count = inv[["name", "iso"]]
    count = count.groupby("iso").count().reset_index().sort_values(by="name", ascending=False)
    count["country"] = count["iso"].apply(lambda x: inv[inv["iso"] == x].iloc[0]["country"])
    fig = go.Figure(data=go.Choropleth(
        locations=count["iso"],
        z=count["name"],
        text=count["country"],
        colorscale=[[0, '#a7aaef'], [0.2, '#353dda'], [1, '#1c2299']],
        autocolorscale=False,
        reversescale=False,
        marker=dict(
            line_color="darkgray",
            line_width=0.5
        ),
        colorbar=dict(
            title='Investigator sites by country'
        )
    ))

    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        showlegend=True,
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        geo=go.layout.Geo(
            projection=dict(type="orthographic"),
            showland=True,
            showcountries=True
        ),
    ),

    fig.data[0].colorbar.x = 0.80

    filterInfo = f"Filters return {round((df.shape[0] / s_base.shape[0]) * 100, 2)}% of the total number of studies"

    return fig, filterInfo


@callback(Output("invDataMapOutput", "data"),
          Output("dfStored", "data"),
          Output("countryInfos", "children"),
          Input("investigators_map", "clickData"),
          Input("categorySelection", "value"),
          Input("stypeSelection", "value"),
          Input("statusSelection", "value"),
          Input("phasesSelection", "value")
          )
def DatatableUpdating(inp, category, stype, status, phase):
    if inp is None:
        df = investigators.copy()
    else:
        df = investigators[investigators["iso"] == inp["points"][0]["location"]].copy()
    if category:
        df = df[df["nct_id"].isin(s_base[s_base.category.isin(category)]["nct_id"])]
    if stype:
        df = df[df["nct_id"].isin(s_base[s_base.study_type.isin(stype)]["nct_id"])]
    if status:
        df = df[df["nct_id"].isin(s_base[s_base.overall_status.isin(status)]["nct_id"])]
    if phase:
        df = df[df["nct_id"].isin(s_base[s_base.study_phases.isin(phase)]["nct_id"])]

    final = df[["name"]].copy()
    final["studies_count"] = 1
    final = final.groupby("name").count().reset_index().sort_values(by="studies_count", ascending=False)
    final["repartition"] = round((final["studies_count"] / df.shape[0]) * 100, 2)
    final["repartition"] = final["repartition"].apply(lambda x: f"{x}%")

    country = inp["points"][0]["text"] if inp else ""

    return final.to_dict('records'), final.to_dict('records'), f"Country selected: {country}"


@callback(Output("studiesDataInvOutput", "data"),
          Input("investigators_map", "clickData"),
          Input("invDataMapOutput", "selected_rows"),
          Input("dfStored", "data"))
def StudiesDatatableUpdating(loc, idx, dfLoc):
    df = s_base.drop(columns=["official_title", "investigators"], axis=1).copy()
    inv = investigators.copy()
    nameRetrieve = pd.DataFrame(dfLoc)

    if loc and idx is None:
        iso = loc["points"][0]["location"]
        df = df[df.nct_id.isin(country[country.iso == iso]["nct_id"])]

    elif idx and loc is None:
        invName = nameRetrieve.loc[idx, "name"].iloc[0]
        df = df[df.nct_id.isin(inv[inv.name == invName]["nct_id"])]

    elif loc and idx:
        invName = nameRetrieve.loc[idx, "name"].iloc[0]
        df = df[df.nct_id.isin(inv[inv.name == invName]["nct_id"])]

        iso = loc["points"][0]["location"]
        df = df[df.nct_id.isin(country[country.iso == iso]["nct_id"])]

    else:
        return df.to_dict('records')

    return df.to_dict('records')