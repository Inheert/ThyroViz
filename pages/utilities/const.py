import pandas as pd
from datetime import datetime, date

s_base = pd.read_csv("script/sql/visualisation/CSV_files/studies.csv")
s_base["study_first_submitted_date"] = pd.to_datetime(s_base["study_first_submitted_date"])
s_base["primary_completion_date"] = pd.to_datetime(s_base["primary_completion_date"])
s_base["completion_date"] = pd.to_datetime(s_base["completion_date"])
s_base.drop(labels="all_conditions", axis=1, inplace=True)

studies = s_base.copy()
studies = studies[studies["overall_status"].isin(["Recruiting", "Not yet recruiting", "Active, not recruiting"])]

sponsors = pd.read_csv("script/sql/visualisation/CSV_files/df_sponsorsName.csv")
# sponsors = sponsors[sponsors["nct_id"].isin(studies.nct_id)]

investigators = pd.read_csv("script/sql/visualisation/CSV_files/df_investigators.csv")
# investigators = investigators[investigators["nct_id"].isin(studies.nct_id)]

intervention_types = pd.read_csv("script/sql/visualisation/CSV_files/df_intervention_types.csv")

country = pd.read_csv("script/sql/visualisation/CSV_files/df_country.csv")

all_category = [x for x in s_base.category.unique()]
all_stype = [x for x in s_base.study_type.unique()]
all_status = [x for x in s_base.overall_status.unique()]
all_phases = [x for x in s_base.study_phases.unique()]

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
    "justifyContent": "center",
    "alignItems": "center",
    'borderBottom': '1px solid #d6d6d6',
    'fontWeight': 'bold',
    "backgroundColor": "rgba(0,0,0,0)"
}

tab_selected_style = {
    "display": "flex",
    "justifyContent": "center",
    "alignItems": "center",
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
}

left_tab_style = {
    "display": "flex",
    "justifyContent": "center",
    "alignItems": "center",
    'borderBottom': '1px solid #d6d6d6',
    'fontWeight': 'bold',
    "backgroundColor": "rgba(0,0,0,0)",
    "borderTopLeftRadius": "15px",
    "borderBottomLeftRadius": "15px"
}

left_tab_selected_style = {
    "display": "flex",
    "justifyContent": "center",
    "alignItems": "center",
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    "borderTopLeftRadius": "15px",
    "borderBottomLeftRadius": "15px"
}

right_tab_style = {
    "display": "flex",
    "justifyContent": "center",
    "alignItems": "center",
    'borderBottom': '1px solid #d6d6d6',
    'fontWeight': 'bold',
    "backgroundColor": "rgba(0,0,0,0)",
    "borderTopRightRadius": "15px",
    "borderBottomRightRadius": "15px"
}

right_tab_selected_style = {
    "display": "flex",
    "justifyContent": "center",
    "alignItems": "center",
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    "borderTopRightRadius": "15px",
    "borderBottomRightRadius": "15px"
}
