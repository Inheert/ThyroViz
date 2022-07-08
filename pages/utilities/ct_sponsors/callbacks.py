import plotly.graph_objects as go
from dash import callback, Output, Input
from pages.utilities.ct_helpers import *
from pages.utilities.ct_sponsors.components import *


@callback(Output("stored_sponsors_df", "data"),
          Input("sponsors_class", "value"),
          Input("studies_category", "value"),
          Input("studies_sub_category", "value"),
          Input("studies_type", "value"),
          Input("studies_status", "value"),
          Input("studies_phases", "value"),
          Input("sort_by", "value"))
def UpdateStoredDataframe(sp_class: list, s_category: list, s_sub_category: list, s_type: list,
                          s_status: list, s_phases: list, sort_by: str):
    df_sponsors = sponsors.copy()
    df_studies = s_base.copy()

    if len(sp_class) > 0:
        df_sponsors = df_sponsors[df_sponsors.new_class.isin(sp_class)]
    if len(s_category) > 0:
        df_studies = df_studies[df_studies.category.isin(s_category)]
    if len(s_sub_category) > 0:
        df_studies = df_studies[df_studies.sub_category.isin(s_sub_category)]
    if len(s_type) > 0:
        df_studies = df_studies[df_studies.study_type.isin(s_type)]
    if len(s_status) > 0:
        df_studies = df_studies[df_studies.overall_status.isin(s_status)]
    if len(s_phases) > 0:
        df_studies = df_studies(df_studies.study_phases.isin(s_phases))

    df_sponsors = df_sponsors[df_sponsors.nct_id.isin(df_studies.nct_id)]
    df_sponsors = df_sponsors.groupby("name").count().reset_index()
    if sort_by == "asc":
        df_sponsors.sort_values(by="name", inplace=True)
    elif sort_by == "desc":
        df_sponsors.sort_values(by="name", ascending=False, inplace=True)
    elif sort_by == "most":
        df_sponsors.sort_values(by="id", ascending=False, inplace=True)
    elif sort_by == "least":
        df_sponsors.sort_values(by="id", inplace=True)

    return df_sponsors.to_dict('records')


@callback(Output("sponsors_pagination", "max_value"),
          Input("stored_sponsors_df", "data"))
def PaginationInitializing(df):
    """

    :param df: the dataframe stocked previously
    :return: the max value for the pagination rounded up to the nearest whole number
    """
    df = pd.DataFrame(df)
    return math.ceil(df.shape[0] / 15)


@callback(Output("sponsors_list", "children"),
          Input("sponsors_pagination", "active_page"),
          Input("stored_sponsors_df", "data"))
def UpdateSponsorsList(page: int, df: dict):
    df = pd.DataFrame(df)
    if df.shape[0] == 0:
        return html.P("No result.", style={"textAlign": "center"})

    page = 1 if page is None else page
    start_range = 15*(page-1)
    end_range = start_range + 15 if df.shape[0] >= start_range+15 else df.shape[0]

    selection_list = []
    for idx in range(start_range, end_range):
        selection = html.Button(children=[
            dbc.Row(
                [
                    dbc.Col(
                        html.Plaintext(df.loc[idx, "name"][0:30]+f"{'...' if len(df.loc[idx, 'name']) > 30 else ''}"),
                        width=2
                    ),
                    dbc.Col(
                        html.Div(
                            html.P(df.loc[idx, "id"]),
                            style={"float": "right",
                                   "alignItems": "center",
                                   }
                        ),
                    )
                ]
            )

        ],
            style={'maxWidth': "24vw", "fontSize": "10px",
                   "height": "4vh"})
        selection_list.append(selection)

    sponsors_list = \
        html.Div(
            children=selection_list,
            className="d-grid gap-1"
        )

    return sponsors_list

#
# @callback(Output("sponsorsClassPie", "figure"),
#           Input("sponsorsClassPie", "figure")
#           )
# def RepartitionPieUpdate(data):
#     df = sponsors
#     df = df.groupby("new_class").count().reset_index().sort_values(by="new_class", ascending=False)
#     df["id"] = df["id"].apply(lambda x: round((x / df["id"].sum()) * 100, 2))
#     fig = go.Figure(data=[go.Pie(
#         labels=df["new_class"],
#         values=df["id"],
#         marker=dict(
#             colors=df["new_class"]
#         )
#     )])
#
#     fig.update_traces(hole=.4, hoverinfo="label+percent")
#
#     fig.update_layout(
#         xaxis=dict(
#             showgrid=False,
#             showline=False,
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
#         margin=dict(l=0, r=0, t=25, b=0),
#         showlegend=True,
#         legend=dict(
#             x=1.2,
#             y=0.85,
#             itemclick=False,
#             # orientation="v",
#             # font=dict(
#             #     size=8
#             # )
#         )
#     )
#     return fig
#
#
# @callback(Output("sp_class", "options"),
#           Output("s_category", "options"),
#           Output("s_sub_category", "options"),
#           Output("s_study_type", "options"),
#           Output("s_study_phases", "options"),
#           Output("s_study_status", "options"),
#           Output("study_time_perspective", "options"),
#           Output("study_int_model", "options"),
#           Output("study_obs_model", "options"),
#           Input("sp_class", "value"),
#           Input("s_category", "value"),
#           Input("s_sub_category", "value"),
#           Input("s_study_type", "value"),
#           Input("s_study_phases", "value"),
#           Input("s_study_status", "value"),
#           Input("study_time_perspective", "value"),
#           Input("study_int_model", "value"),
#           Input("study_obs_model", "value"),
#           )
# def UpdateSponsorsDataFrameFilters(sp_class, category, sub_category, stype, sphases, sstatus, stime_perspective,
#                                    s_int_model, s_obs_model):
#     _s_base = s_base.copy()
#     _sponsors = sponsors.copy()
#
#     if sp_class:
#         _sponsors = _sponsors[_sponsors.new_class.isin(sp_class if isinstance(sp_class, list) else [sp_class])]
#     if category:
#         _s_base = _s_base[_s_base.category.isin(category if isinstance(category, list) else [category])]
#     if sub_category:
#         _s_base = _s_base[_s_base.sub_category.isin(sub_category if isinstance(sub_category, list) else [sub_category])]
#     if stype:
#         _s_base = _s_base[_s_base.study_type.isin(stype if isinstance(stype, list) else [stype])]
#     if sphases:
#         _s_base = _s_base[_s_base.study_phases.isin(sphases if isinstance(sphases, list) else [sphases])]
#     if sstatus:
#         _s_base = _s_base[_s_base.overall_status.isin(sstatus if isinstance(sstatus, list) else [sstatus])]
#     if stime_perspective:
#         _s_base = _s_base[_s_base.time_perspective.isin(
#             stime_perspective if isinstance(stime_perspective, list) else [stime_perspective])]
#     if s_int_model:
#         _s_base = _s_base[
#             _s_base.intervention_model.isin(s_int_model if isinstance(s_int_model, list) else [s_int_model])]
#     if s_obs_model:
#         _s_base = _s_base[
#             _s_base.observational_model.isin(s_obs_model if isinstance(s_obs_model, list) else [s_obs_model])]
#
#     return [x for x in _sponsors.new_class.sort_values().unique()] if not sp_class else all_sponsors_class, \
#            [x for x in _s_base.category.sort_values().unique()], \
#            [x for x in _s_base.sub_category.sort_values().unique()], \
#            [x for x in _s_base.study_type.sort_values().unique()], \
#            [x for x in _s_base.study_phases.sort_values().unique()], \
#            [x for x in _s_base.overall_status.sort_values().unique()], \
#            [x for x in _s_base.time_perspective.sort_values().unique()], \
#            [x for x in _s_base.intervention_model.sort_values().unique()], \
#            [x for x in _s_base.observational_model.sort_values().unique()]
