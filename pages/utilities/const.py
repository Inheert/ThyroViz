import pandas as pd
from datetime import datetime, date

s_base = pd.read_csv("script/sql/visualisation/CSV_files/studies.csv")
s_base["study_first_submitted_date"] = pd.to_datetime(s_base["study_first_submitted_date"])
s_base["completion_date"] = pd.to_datetime(s_base["completion_date"])

studies = s_base.copy()
studies = studies[studies["overall_status"].isin(["Recruiting", "Not yet recruiting", "Active, not recruiting"])]

sponsors = pd.read_csv("script/sql/visualisation/CSV_files/df_sponsorsName.csv")
sponsors = sponsors[sponsors["nct_id"].isin(studies.nct_id)]

investigators = pd.read_csv("script/sql/visualisation/CSV_files/df_investigators.csv")
investigators = investigators[investigators["nct_id"].isin(studies.nct_id)]

all_category = [x for x in s_base.category.unique()]

card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
}

card_icon2 = {
    "color": "#454545",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
}

tabs_styles = {
    'height': '44px',
    "width": "1000px"
}
tab_style = {
    "display": "flex",
    "justify-content": "center",
    "align-items": "center",
    'borderBottom': '1px solid #d6d6d6',
    'fontWeight': 'bold'
}

tab_selected_style = {
    "display": "flex",
    "justify-content": "center",
    "align-items": "center",
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
}
