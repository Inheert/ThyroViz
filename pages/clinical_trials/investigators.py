import dash
from dash import Input, Output, callback

from pages.utilities.ct_investigators.components import *
from pages.utilities.ct_helpers import *

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
                        investigatorsLocations
                    ]
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


@callback(Output("invLocations", "children"),
          Input("invDataMapOutput", "selected_rows"),
          Input("dfStored", "data"))
def DisplayInvestigatorsLocations(idx, dfStored):
    df = pd.DataFrame(dfStored)

    if idx:
        row = dict(investigators[investigators.name == df.loc[idx, "name"].iloc[0]].iloc[0])
        rows = investigators[investigators.name == df.loc[idx, "name"].iloc[0]]

        table = dash_table.DataTable(
                            data=rows.to_dict("records"),
                            columns=[{"name": i, "id": i} for i in rows[["city", "state", "country", "zip", "continent"]].columns],
                            page_size=15,
                            filter_action="native",
                            sort_action="native",
                            row_selectable="single",
                            style_cell={
                                'height': 'auto',
                                # all three widths are needed
                                'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',
                                'whiteSpace': 'normal'
                            },
                            style_header={
                                'backgroundColor': "#0D6986",
                                "color": "white",
                                "fontWeight": 900,
                                "fontSize": "12px"
                            },
                            style_table={
                                'borderRadius': '15px',
                                'overflow': 'hidden',
                                'overflowX': 'auto'
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

    else:
        return None

@callback(Output("name", "children"),
          Output("city", "children"),
          Output("state", "children"),
          Output("country", "children"),
          Output("continent", "children"),
          Input("invDataMapOutput", "selected_rows"),
          Input("dfStored", "data"))
def InvestigatorInfosUpdate(idx, dfLoc):
    df = pd.DataFrame(dfLoc)
    if idx:
        row = dict(investigators[investigators.name == df.loc[idx, "name"].iloc[0]].iloc[0])
        rows = investigators[investigators.name == df.loc[idx, "name"].iloc[0]]
        city, state, country, continent = [x for x in rows.city.unique()], [x for x in rows.state.unique()], [x for x in rows.country.unique()], [x for x in rows.continent.unique()]

        return f"**Name:** {row['name']}", f"**City:** {row['city']}", f"**State:** {row['state']}", f"**Country:** {row['country']}", f"**Continent:** {row['continent']}"

    return "**Name:** ", "**City:** ", "**State:** ", "**Country:** ", "**Continent:** "


@callback(Output("invDataMapOutput", "selected_rows"),
          Input("categorySelection", "value"),
          Input("stypeSelection", "value"),
          Input("statusSelection", "value"),
          Input("phasesSelection", "value"))
def SelectedRowVerification(*args):
    return []


@callback(Output("investigators_map", "figure"),
          Output("filtersInfos", "children"),
          Input("categorySelection", "value"),
          Input("stypeSelection", "value"),
          Input("statusSelection", "value"),
          Input("phasesSelection", "value"),
          Input("subCategorySelection", "value"))
def GeoInvestigatorsUpdate(cat, stype, status, phase, sub_category):
    inv = investigators.copy()
    df = s_base.copy()

    if cat:
        inv = inv[inv["nct_id"].isin(s_base[s_base.category.isin(cat)]["nct_id"])]
        df = df[df.category.isin(cat)]
    if stype:
        inv = inv[inv["nct_id"].isin(s_base[s_base.study_type.isin(stype)]["nct_id"])]
        df = df[df.study_type.isin(stype)]
    if status:
        inv = inv[inv["nct_id"].isin(s_base[s_base.overall_status.isin(status)]["nct_id"])]
        df = df[df.overall_status.isin(status)]
    if phase:
        df = df[df.study_phases.isin(phase)]
        inv = inv[inv["nct_id"].isin(s_base[s_base.study_phases.isin(phase)]["nct_id"])]
    if sub_category:
        df = df[df.sub_category.isin(sub_category)]
        inv = inv[inv["nct_id"].isin(s_base[s_base.sub_category.isin(sub_category)]["nct_id"])]

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

    _s_base = s_base.copy()

    _s_base.drop_duplicates(subset=["nct_id", "category"], keep="first", inplace=True)
    df.drop_duplicates(subset=["nct_id", "category"], keep="first", inplace=True)

    filterInfo = f"Filters return {round((df.nct_id.shape[0] / _s_base.nct_id.shape[0]) * 100, 2)}% of the total number of studies"

    return fig, filterInfo


@callback(Output("invDataMapOutput", "data"),
          Output("dfStored", "data"),
          Output("countryInfos", "children"),
          Input("investigators_map", "clickData"),
          Input("categorySelection", "value"),
          Input("stypeSelection", "value"),
          Input("statusSelection", "value"),
          Input("phasesSelection", "value"),
          Input("subCategorySelection", "value")
          )
def DatatableUpdating(inp, cat, stype, status, phase, sub_category):
    if inp is None:
        df = investigators.copy()
    else:
        df = investigators[investigators["iso"] == inp["points"][0]["location"]].copy()

    if cat:
        df = df[df["nct_id"].isin(s_base[s_base.category.isin(cat)]["nct_id"])]
    if stype:
        df = df[df["nct_id"].isin(s_base[s_base.study_type.isin(stype)]["nct_id"])]
    if status:
        df = df[df["nct_id"].isin(s_base[s_base.overall_status.isin(status)]["nct_id"])]
    if phase:
        df = df[df["nct_id"].isin(s_base[s_base.study_phases.isin(phase)]["nct_id"])]
    if sub_category:
        df = df[df["nct_id"].isin(s_base[s_base.sub_category.isin(sub_category)]["nct_id"])]

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

    if loc and len(idx) == 0:
        iso = loc["points"][0]["location"]
        df = df[df.nct_id.isin(country[country.iso == iso]["nct_id"])]

    elif len(idx) > 0 and loc is None:
        invName = nameRetrieve.loc[idx[0], "name"]
        df = df[df.nct_id.isin(inv[inv.name == invName]["nct_id"])]

    elif loc and len(idx) > 0:
        invName = nameRetrieve.loc[idx[0], "name"]
        df = df[df.nct_id.isin(inv[inv.name == invName]["nct_id"])]

        iso = loc["points"][0]["location"]
        df = df[df.nct_id.isin(country[country.iso == iso]["nct_id"])]

    else:
        return df.to_dict('records')

    return df.to_dict('records')


@callback(Output("subCategorySelection", "options"),
          Input("categorySelection", "value"))
def UpdateOptionsForSubCategory(category: list):
    df = s_base[["category", "sub_category"]].copy()

    if category and len(category) > 0:

        df["keep"] = df["category"].apply(lambda x: True if x in category else False)
        df = df[df.keep == True]

    return [x for x in df.sort_values(by=["category", "sub_category"])["sub_category"].unique()]

