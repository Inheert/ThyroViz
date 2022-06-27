import plotly.graph_objects as go
from dash import callback, Output, Input
from pages.utilities.ct_helpers import *
from pages.utilities.ct_sponsors.components import *


@callback(Output("sponsorsClassPie", "figure"),
          Input("sponsorsClassPie", "figure")
          )
def RepartitionPieUpdate(data):
    df = sponsors
    df = df.groupby("new_class").count().reset_index().sort_values(by="new_class", ascending=False)
    df["Unnamed: 0"] = df["Unnamed: 0"].apply(lambda x: round((x/df["Unnamed: 0"].sum())*100, 2))
    fig = go.Figure(data=[go.Pie(
        labels=df["new_class"],
        values=df["Unnamed: 0"],
        marker=dict(
            colors=df["new_class"]
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
            x=1.2,
            y=0.85,
            itemclick=False,
            # orientation="v",
            # font=dict(
            #     size=8
            # )
        )
    )
    return fig


@callback(Output("sp_class", "options"),
          Output("s_category", "options"),
          Output("s_sub_category", "options"),
          Output("s_study_type", "options"),
          Output("s_study_phases", "options"),
          Output("s_study_status", "options"),
          Output("study_time_perspective", "options"),
          Output("study_int_model", "options"),
          Output("study_obs_model", "options"),
          Input("sp_class", "value"),
          Input("s_category", "value"),
          Input("s_sub_category", "value"),
          Input("s_study_type", "value"),
          Input("s_study_phases", "value"),
          Input("s_study_status", "value"),
          Input("study_time_perspective", "value"),
          Input("study_int_model", "value"),
          Input("study_obs_model", "value"),
          )
def UpdateSponsorsDataFrameFilters(sp_class, category, sub_category, stype, sphases, sstatus, stime_perspective, s_int_model, s_obs_model):
    _s_base = s_base.copy()
    _sponsors = sponsors.copy()

    if sp_class:
        _sponsors = _sponsors[_sponsors.new_class.isin(sp_class if isinstance(sp_class, list) else [sp_class])]
    if category:
        _s_base = _s_base[_s_base.category.isin(category if isinstance(category, list) else [category])]
    if sub_category:
        _s_base = _s_base[_s_base.sub_category.isin(sub_category if isinstance(sub_category, list) else [sub_category])]
    if stype:
        _s_base = _s_base[_s_base.study_type.isin(stype if isinstance(stype, list) else [stype])]
    if sphases:
        _s_base = _s_base[_s_base.study_phases.isin(sphases if isinstance(sphases, list) else [sphases])]
    if sstatus:
        _s_base = _s_base[_s_base.overall_status.isin(sstatus if isinstance(sstatus, list) else [sstatus])]
    if stime_perspective:
        _s_base = _s_base[_s_base.time_perspective.isin(stime_perspective if isinstance(stime_perspective, list) else [stime_perspective])]
    if s_int_model:
        _s_base = _s_base[_s_base.intervention_model.isin(s_int_model if isinstance(s_int_model, list) else [s_int_model])]
    if s_obs_model:
        _s_base = _s_base[_s_base.observational_model.isin(s_obs_model if isinstance(s_obs_model, list) else [s_obs_model])]

    return [x for x in _sponsors.new_class.sort_values().unique()] if not sp_class else all_sponsors_class, \
           [x for x in _s_base.category.sort_values().unique()], \
           [x for x in _s_base.sub_category.sort_values().unique()], \
           [x for x in _s_base.study_type.sort_values().unique()], \
           [x for x in _s_base.study_phases.sort_values().unique()], \
           [x for x in _s_base.overall_status.sort_values().unique()], \
           [x for x in _s_base.time_perspective.sort_values().unique()], \
           [x for x in _s_base.intervention_model.sort_values().unique()], \
           [x for x in _s_base.observational_model.sort_values().unique()]
