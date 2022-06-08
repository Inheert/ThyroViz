import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
import numpy as np
import plotly.graph_objects as go
from geopy import Nominatim
from pages.utilities.const import *

newStudiesTitle = \
    dbc.Row(
        [
            dbc.Col(
                dbc.Row(
                    [
                        dbc.Col(html.H5("New studies this"), width="auto"),
                        dbc.Col(
                            dcc.Dropdown(
                                id="newStudiesDate",
                                options=["day", "week", "month", "year"],
                                value="month",
                                multi=False,
                                clearable=False,
                                style={
                                    "width": "5vw",
                                    "marginTop": "0.5vh",
                                }
                            ),
                        ),
                        dbc.Col(
                            dbc.Button(children="More informations",
                                       id="newStudiesInfos",
                                       style={"marginLeft": "9vw"})
                        ),
                        html.Hr(style={"marginTop": "1.5vh", "marginBottom": "1.5vh"})
                    ]
                ),
            ),
        ]
    )

newStudiesDatatable = \
    dash_table.DataTable(
        id="newStudiesDatatable",
        data=s_base.drop_duplicates(subset="nct_id").to_dict('records'),
        columns=[{"name": i, "id": i} for i in
                 s_base[["nct_id", "study_type", "overall_status", "study_first_submitted_date"]].columns],
        page_size=10,
        filter_action="native",
        sort_action="native",
        row_selectable="single",
        style_cell={
            'height': 'auto',
            # all three widths are needed
            'minWidth': '200px', 'width': '200px', 'maxWidth': '200px',
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

newStudiesModal = \
    html.Div(id="newStudiesModal")

completedStudiesTitle = \
    dbc.Row(
        [
            dbc.Col(
                dbc.Row(
                    [
                        dbc.Col(html.H5("Completed studies this"), width="auto"),
                        dbc.Col(
                            dcc.Dropdown(
                                id="CompletedStudiesDate",
                                options=["day", "week", "month", "year"],
                                value="month",
                                multi=False,
                                clearable=False,
                                style={
                                    "width": "5vw",
                                    "marginTop": "0.5vh",
                                }
                            ),
                        ),
                        dbc.Col(
                            dbc.Button(children="More informations",
                                       id="completedStudiesInfos",
                                       style={"marginLeft": "7vw"})
                        ),
                        html.Hr(style={"marginTop": "1.5vh", "marginBottom": "1.5vh"})
                    ]
                ),
            ),
        ]
    )

completedStudiesDatatable = \
    dash_table.DataTable(
        id="completedStudiesDatatable",
        data=s_base.drop_duplicates(subset="nct_id").to_dict('records'),
        columns=[{"name": i, "id": i} for i in
                 s_base[["nct_id", "study_type", "overall_status", "completion_date"]].columns],
        page_size=10,
        filter_action="native",
        sort_action="native",
        row_selectable="single",
        style_cell={
            'height': 'auto',
            # all three widths are needed
            'minWidth': '200px', 'width': '200px', 'maxWidth': '200px',
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

completedStudiesModal = \
    html.Div(id="completedStudiesModal")


allStudiesHeader = \
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                options=[x for x in all_category],
                placeholder="Category...",
                multi=True,
            )
        ]),
        dbc.Col([
            dcc.Dropdown(
                options=[x for x in s_base.sub_category.unique()],
                placeholder="Sub-category..."
            )
        ]),
        dbc.Col([
            dcc.Dropdown(
                options=[x for x in all_stype],
                placeholder="Study type...",
            )
        ]),
        dbc.Col([
            dcc.Dropdown(
                options=[x for x in all_phases],
                placeholder="Study phases..."
            )
        ]),
        dbc.Col([
            dcc.Dropdown(
                options=[x for x in all_status],
                placeholder="Study status..."
            )
        ])
    ])

allStudiesDatatable = \
    dash_table.DataTable(
        id="allStudiesDatatable",
        data=s_base.to_dict('records'),
        columns=[{"name": i, "id": i} for i in
                 s_base.drop(columns=["Unnamed: 0", "intervention_types", "investigators", "sponsors_name", "downcase_mesh_term", "minimum_age_num", "maximum_age_num", "intervention_model", "observational_model", "time_perspective"]).columns],
        page_size=10,
        filter_action="native",
        sort_action="native",
        row_selectable="single",
        style_cell={
            'height': 'auto',
            # all three widths are needed
            'minWidth': '150px', 'width': '150px', 'maxWidth': '200px',
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


def ModalStudiesInfo(row, isOpen, df=None):
    if df:
        _s_base = pd.DataFrame(df).sort_values(by="category")
        row = _s_base.loc[row].reset_index(drop=True)
    else:
        _s_base = s_base.sort_values(by="category")
        row = _s_base.loc[row].reset_index(drop=True)

    df = s_base[s_base["nct_id"] == row["nct_id"][0]].reset_index(drop=True).copy()
    sp = sponsors[sponsors["nct_id"] == row["nct_id"][0]]

    inv = investigators[investigators["nct_id"] == row["nct_id"][0]].__deepcopy__()
    inv["city_country"] = inv[["city", "country"]].agg(", ".join, axis=1)

    geoloc = Nominatim(user_agent="ThyroResearch", timeout=3)

    inv["lat"] = inv["city_country"].apply(lambda x: geoloc.geocode(x).latitude)
    inv["long"] = inv["city_country"].apply(lambda x: geoloc.geocode(x).longitude)

    for col in row:
        row[col] = row[col].apply(lambda x: None if x is np.nan or x is pd.NaT or x is None else x)

    data = [go.Scattergeo(
        lat=inv["lat"],
        lon=inv["long"],
        text=inv["name"],
        mode="markers",
        hovertemplate=
        "<b>%{text}</b><br><br>"
    )]

    layout = go.Layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=350,
        width=350,
        showlegend=False,
        geo=go.layout.Geo(
            projection=dict(type="orthographic"),
            showland=True,
            showcountries=True
        )
    )

    fig = go.Figure(data=data, layout=layout)

    layout = \
        dbc.Modal(
            [
                dbc.ModalHeader(row.nct_id),
                dbc.ModalTitle(
                    dcc.Link(children=f"{row.official_title[0]}", href=df.URL.unique()[0], target="_blank") if
                    row.official_title[0] is not None else dcc.Link(children=f"{row.brief_title[0]}",
                                                                    href=df.URL.unique()[0], target="_blank"),
                    id="modalTitle",
                    style={
                        "fontSize": '25px',
                        "fontWeight": "bold",
                        "marginLeft": "5px"
                    }),
                dbc.ModalBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Markdown(f'''
                                        **Funded by:** {df.funded_bys.unique()[0]}
                                        \n
                                        **Study type:** {df.study_type.unique()[0]}
                                        \n
                                        **Overall status:** {df.overall_status.unique()[0]}
                                        \n
                                        **Study phases:** {df.study_phases.unique()[0]}
                                        \n
                                        **Observational model:** {df.observational_model.unique()[0]}
                                        \n
                                        **Intervention model:** {df.intervention_model.unique()[0]}
                                        \n
                                        **Enrollment:** {int(df.enrollment.unique()[0])}
                                        \n
                                        **Minimum age:** {int(df.minimum_age_num.unique()[0])} years old
                                        \n
                                        **Maximum age:** {int(df.maximum_age_num.unique()[0])} years old
                                        \n
                                        **Time perspective:** {df.time_perspective.unique()[0]}
                                        \n
                                        **First submitted date:** {df.study_first_submitted_date[0].strftime("%Y-%m-%d")}
                                        \n
                                        **Estimated primary completion date:** {'Not provided' if df.primary_completion_date[0] is pd.NaT else df.primary_completion_date[0].strftime("%Y-%m-%d")}
                                        \n
                                        **Estimated completion date:** {'Not provided' if df.completion_date[0] is pd.NaT else df.completion_date[0].strftime("%Y-%m-%d")}
                                        ''')
                                    ],
                                    style={
                                        "display": "flex",
                                        "alignItems": "center",
                                        "justifyContent": "left",
                                        "horizontalAlign": "center",
                                    }
                                ),
                                dbc.Col(
                                    [
                                        dcc.Graph(
                                            figure=fig,
                                            config={
                                                'displayModeBar': False,
                                            }
                                        ),
                                    ],
                                    style={
                                        "marginLeft": "20px",
                                        "display": "flex",
                                        "alignItems": "center",
                                        "justifyContent": "center",
                                        "horizontalAlign": "center"
                                    }
                                )
                            ],
                            style={
                                "display": "flex",
                                "alignItems": "center",
                                "justifyContent": "center",
                                "horizontalAlign": "center"
                            }
                        ),
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Accordion([
                                    dbc.AccordionItem(title="Categories",
                                                      children=[
                                                          html.Div([
                                                            dbc.Row(
                                                                [
                                                                    dbc.Col([
                                                                        dbc.Button(children=category,
                                                                                   id=f"{category}Button"),
                                                                        dbc.Popover(
                                                                            children=f"{[x for x in df[df.category == category]['sub_category'].unique()]}".replace("[", "").replace("]", ""),
                                                                            target=f"{category}Button",
                                                                            body=True, trigger="hover", placement="bottom",
                                                                            style={"fontSize": "1.3vh"}
                                                                        )
                                                                    ], width="auto")
                                                                    for category in df.category.unique()
                                                                ]
                                                            )
                                                          ])
                                                      ]),
                                    dbc.AccordionItem(title="Sponsors"),
                                    dbc.AccordionItem(title="Investigators sites")
                                ]),
                                dbc.Col(
                                    [
                                        dash_table.DataTable(
                                            data=df.to_dict('records'),
                                            columns=[
                                                {"name": i, "id": i}
                                                for i in df[["category", "sub_category"]].columns
                                            ],
                                            style_data={
                                                "whiteSpace": "normal",
                                                "height": "auto"
                                            }
                                        )
                                    ],
                                    width="auto"
                                ),
                                dbc.Col(
                                    [
                                        dash_table.DataTable(
                                            data=sp.to_dict('records'),
                                            columns=[
                                                {"name": i, "id": i}
                                                for i in sp[["name", "lead_or_collaborator", "new_class"]]
                                            ],
                                            style_data={
                                                "whiteSpace": "normal",
                                                "height": "auto"
                                            }
                                        ),
                                        html.Br(),
                                        dash_table.DataTable(
                                            data=inv.to_dict('records'),
                                            columns=[
                                                {"name": i, "id": i}
                                                for i in inv[["name"]]
                                            ],
                                            style_data={
                                                "whiteSpace": "normal",
                                                "height": "auto"
                                            }
                                        )
                                    ],
                                    width="auto"
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                    ],
                                    width="auto"
                                )
                            ]
                        )
                    ]
                )
            ],
            id="studyModal",
            is_open=isOpen,
            size="xl"
        )

    return layout
