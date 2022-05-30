import dash
from dash import Input, Output, State, callback, dash_table, html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from plotly.subplots import make_subplots

from pages.utilities.const import *

dash.register_page(__name__)

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(id="categorySelection",
                                     options=[x for x in all_category],
                                     multi=True),
                        dcc.Dropdown(id="stypeSelection",
                                     options=[x for x in all_stype],
                                     multi=True),
                        dcc.Dropdown(id="statusSelection",
                                     options=[x for x in all_status],
                                     multi=True),
                        dcc.Dropdown(id="phasesSelection",
                                     options=['Unknow' if x is None else x for x in all_phases],
                                     multi=True),
                    ]
                ),
                dbc.Col(
                    [
                        dcc.Graph(id="investigators_map",
                                  config={
                                      'displayModeBar': False,
                                  }
                                  ),
                    ],
                    width=7
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    dbc.Row(dbc.Col(id="mapOutput1", width="auto"),),
                                ]
                            ),
                            style={"backgroundColor": "hsl(247.74, 52.54%, 98.43%)",
                                   "borderRadius": "15px",
                                   "marginTop": "15px"}
                        )
                    ],
                    width="auto"
                ),
            ]
        ),
    ]
),

@callback(Output("investigators_map", "figure"),
          Input("categorySelection", "value"),
          Input("stypeSelection", "value"),
          Input("statusSelection", "value"),
          Input("phasesSelection", "value"))
def GeoInvestigatorsUpdate(category, stype, status, phase):
    inv = investigators.copy()

    if category:
        inv = inv[inv["nct_id"].isin(s_base[s_base.category.isin(category)]["nct_id"])]
    if stype:
        inv = inv[inv["nct_id"].isin(s_base[s_base.study_type.isin(stype)]["nct_id"])]
    if status:
        inv = inv[inv["nct_id"].isin(s_base[s_base.overall_status.isin(status)]["nct_id"])]
    if phase:
        print(phase)
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

    return fig


@callback(Output("mapOutput1", "children"),
          Input("investigators_map", "clickData"))
def DatatableUpdating(inp):
    if inp is None:
        inv = investigators.copy()
    else:
        inv = investigators[investigators["iso"] == inp["points"][0]["location"]].copy()

    count = inv[["name"]].copy()
    count["studies_count"] = 1
    count = count.groupby("name").count().reset_index().sort_values(by="studies_count", ascending=False)
    count["repartition"] = round((count["studies_count"]/inv.shape[0])*100, 2)
    count["repartition"] = count["repartition"].apply(lambda x: f"{x}%")
    table = \
        dash_table.DataTable(
            data=count.to_dict('records'),
            columns=[{"name": i, "id": i} for i in
                     count[["name", "studies_count", "repartition"]].columns],
            page_size=10,
            row_selectable="single",
            filter_action="native",
            sort_action="native",
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
