import datetime
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, dash_table, html, dcc
from dateutil.relativedelta import relativedelta

from pages.utilities.ct_studies.components import *


@callback(Output("newStudiesDatatable", "data"),
          Input("newStudiesDate", "value"))
def UpdateNewStudiesDatatable(selection):
    df = s_base.copy()
    now = datetime.now().strftime("%Y-%m-%d")
    now = datetime.strptime(now, "%Y-%m-%d")
    if selection == "day":
        df = df[df["study_first_submitted_date"] >= now - relativedelta(days=1)]
        pass
    elif selection == "week":
        df = df[df["study_first_submitted_date"] >= now - relativedelta(days=7)]
        pass
    elif selection == "month":
        df = df[df["study_first_submitted_date"] >= now - relativedelta(months=1)]
        pass
    elif selection == "year":
        df = df[df["study_first_submitted_date"] >= datetime.strptime(f"{now.year}-01-01", "%Y-%m-%d")]
        pass

    return df.drop_duplicates(subset="nct_id").sort_values(by="study_first_submitted_date", ascending=False).to_dict(
        'records')


@callback(Output("newStudiesModal", "children"),
          Output("newStudiesInfos", "n_clicks"),
          Input("newStudiesDatatable", "selected_rows"),
          Input("newStudiesInfos", "n_clicks"),
          Input("newStudiesDatatable", "data"))
def NewStudiesModal(data, n_clicks, df):
    if n_clicks and data:
        return ModalStudiesInfo(data if data is not None else [0], True, df), None
    else:
        return None, None


@callback(Output("completedStudiesDatatable", "data"),
          Input("CompletedStudiesDate", "value"))
def UpdateCompletedStudiesDatatable(selection):
    df = s_base.copy()
    now = datetime.now().strftime("%Y-%m-%d")
    now = datetime.strptime(now, "%Y-%m-%d")
    df = df[df["completion_date"] <= now]
    if selection == "day":
        df = df[df["completion_date"] >= now - relativedelta(days=1)]
        pass
    elif selection == "week":
        df = df[df["completion_date"] >= now - relativedelta(days=7)]
        pass
    elif selection == "month":
        df = df[df["completion_date"] >= now - relativedelta(months=1)]
        pass
    elif selection == "year":
        df = df[df["completion_date"] >= datetime.strptime(f"{now.year}-01-01", "%Y-%m-%d")]
        pass

    return df.drop_duplicates(subset="nct_id").sort_values(by="completion_date", ascending=False).to_dict('records')


@callback(Output("completedStudiesModal", "children"),
          Output("completedStudiesInfos", "n_clicks"),
          Input("completedStudiesDatatable", "selected_rows"),
          Input("completedStudiesInfos", "n_clicks"),
          Input("completedStudiesDatatable", "data"))
def CompletedStudiesModal(data, n_clicks, df):
    if n_clicks and data:
        return ModalStudiesInfo(data if data is not None else [0], True, df), None
    else:
        return None, None


@callback(Output("category", "options"),
          Output("sub_category", "options"),
          Output("study_type", "options"),
          Output("study_phases", "options"),
          Output("study_status", "options"),
          Input("category", "value"),
          Input("sub_category", "value"),
          Input("study_type", "value"),
          Input("study_phases", "value"),
          Input("study_status", "value")
          )
def UpdateDataframeFilters(category, sub_category, stype, sphases, sstatus):
    _s_base = s_base.copy()

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

    return [x for x in _s_base.category.sort_values().unique()], \
           [x for x in _s_base.sub_category.sort_values().unique()], \
           [x for x in _s_base.study_type.sort_values().unique()], \
           [x for x in _s_base.study_phases.sort_values().unique()], \
           [x for x in _s_base.overall_status.sort_values().unique()], \


@callback(Output("allStudiesDatatable", "data"),
          Input("category", "value"),
          Input("sub_category", "value"),
          Input("study_type", "value"),
          Input("study_phases", "value"),
          Input("study_status", "value"))
def UpdateStudiesDataframe(category, sub_category, stype, sphases, sstatus):
    _s_base = s_base.copy()

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

    return _s_base.to_dict('records')


@callback(Output("allStudiesModal", "children"),
          Output("allStudiesInfos", "n_clicks"),
          Input("allStudiesDatatable", "selected_rows"),
          Input("allStudiesInfos", "n_clicks"),
          Input("allStudiesDatatable", "data"))
def CompletedStudiesModal(data, n_clicks, df):
    if n_clicks and data:
        return ModalStudiesInfo(data if data is not None else [0], True, df), None
    else:
        return None, None
