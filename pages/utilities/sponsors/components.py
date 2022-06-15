from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc

from pages.utilities.helpers import *


sponsorsClassPieChart = \
    dbc.Card(
        dbc.CardBody(
            [
                dcc.Graph(id="sponsorsClassPie", config={"displayModeBar": False},
                          style={"width": "25vw"})
            ]
        ),
        class_name="card mb-4 border-1",
        style={"backgroundColor": "hsl(247.74, 52.54%, 98.43%)",
               "borderRadius": "15px",
               }
    )

filters = \
    dbc.Card(
        dbc.CardBody(
            [
                html.Plaintext("Sponsors class:"),
                dcc.Dropdown(
                    options=all_sponsors_class,
                    id="sp_class"
                ),
                html.Br(),

                html.Plaintext("Studies category:"),
                dcc.Dropdown(
                    options=all_category,
                    id="s_category"
                ),
                html.Br(),

                html.Plaintext("Studies sub-category:"),
                dcc.Dropdown(
                    options=all_sub_category,
                    id="s_sub_category"
                ),
                html.Br(),

                html.Plaintext("Studies type:"),
                dcc.Dropdown(
                    options=all_stype,
                    id="s_study_type"
                ),
                html.Br(),

                html.Plaintext("Studies phases:"),
                dcc.Dropdown(
                    options=all_phases,
                    id="s_study_phases"
                ),
                html.Br(),

                html.Plaintext("Studies status:"),
                dcc.Dropdown(
                    options=all_status,
                    id="s_study_status"
                ),
                html.Br(),

                html.Plaintext("Time perspective:"),
                dcc.Dropdown(
                    options=all_time_perspective,
                    id="study_time_perspective"
                ),
                html.Br(),

                html.Plaintext("Intervention model:"),
                dcc.Dropdown(
                    options=all_int_models,
                    id="study_int_model"
                ),
                html.Br(),

                html.Plaintext("Observational model:"),
                dcc.Dropdown(
                    options=all_obs_models,
                    id="study_obs_model"
                ),
                html.Br(),
            ]
        ),
        style={
            "borderRadius": "15px"
        }
    )

sponsorsDatatable = \
    dash_table.DataTable(
        id="sponsorsDatatable",
        data=sponsors.to_dict('records'),
        columns=[{"name": i, "id": i} for i in
                 sponsors[["name", 'new_class']].columns],
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
