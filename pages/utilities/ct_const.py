import pandas as pd
from datetime import datetime, date

s_base = pd.read_csv("script/clinical_trials/sql/visualisation/CSV_files/studies.csv", index_col=[0])
s_base["study_first_submitted_date"] = pd.to_datetime(s_base["study_first_submitted_date"])
s_base["primary_completion_date"] = pd.to_datetime(s_base["primary_completion_date"])
s_base["completion_date"] = pd.to_datetime(s_base["completion_date"])
s_base.drop(labels="all_conditions", axis=1, inplace=True)

studies = s_base.copy()
studies = studies[studies["overall_status"].isin(["Recruiting", "Not yet recruiting", "Active, not recruiting"])]

sponsors = pd.read_csv("script/clinical_trials/sql/visualisation/CSV_files/df_sponsorsName.csv", index_col=[0])
# ct_sponsors = ct_sponsors[ct_sponsors["nct_id"].isin(ct_studies.nct_id)]

investigators = pd.read_csv("script/clinical_trials/sql/visualisation/CSV_files/df_investigators.csv", index_col=[0])
# ct_investigators = ct_investigators[ct_investigators["nct_id"].isin(ct_studies.nct_id)]

intervention_types = pd.read_csv("script/clinical_trials/sql/visualisation/CSV_files/df_intervention_types.csv", index_col=[0])

country = pd.read_csv("script/clinical_trials/sql/visualisation/CSV_files/df_country.csv")

all_category = [x for x in s_base.category.sort_values().unique()]
all_sub_category = [x for x in s_base.sub_category.sort_values().unique()]
all_stype = [x for x in s_base.study_type.sort_values().unique()]
all_status = [x for x in s_base.overall_status.sort_values().unique()]
all_phases = [x for x in s_base.study_phases.sort_values().unique()]
all_time_perspective = [x for x in s_base.time_perspective.sort_values().unique()]
all_int_models = [x for x in s_base.intervention_model.sort_values().unique()]
all_obs_models = [x for x in s_base.observational_model.sort_values().unique()]

all_sponsors_class = [x for x in sponsors.new_class.sort_values().unique()]

card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": "2vmax",
    "margin": "auto",
}

card_icon2 = {
    "color": "#454545",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
}

tabs_styles = {
    'height': '44vh',
    "width": "60vw"
}
tab_style = {
    "display": "flex",
    "justifyContent": "center",
    "alignItems": "center",
    'borderBottom': '1px solid #d6d6d6',
    'fontWeight': 'bold',
    "backgroundColor": "rgba(0,0,0,0)",
    'fontSize': '0.8vmax',
}

tab_selected_style = {
    "display": "flex",
    "justifyContent": "center",
    "alignItems": "center",
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'fontSize': '0.8vmax',
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
