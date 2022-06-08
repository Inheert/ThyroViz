import datetime
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, dash_table, html, dcc
from dateutil.relativedelta import relativedelta

from pages.utilities.studies.components import *

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

    return df.drop_duplicates(subset="nct_id").sort_values(by="study_first_submitted_date", ascending=False).to_dict('records')


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