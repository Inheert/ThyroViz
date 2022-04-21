import pandas as pd
from datetime import datetime

s_base = pd.read_csv("script/sql/visualisation/CSV_files/studies.csv")
s_base["study_first_submitted_date"] = pd.to_datetime(s_base["study_first_submitted_date"])
s_base["completion_date"] = pd.to_datetime(s_base["completion_date"])

studies = s_base.copy()
studies = studies[studies["overall_status"].isin(["Recruiting", "Not yet recruiting", "Active, not recruiting"])]

sponsors = pd.read_csv("script/sql/visualisation/CSV_files/df_sponsorsName.csv")
sponsors = sponsors[sponsors["nct_id"].isin(studies.nct_id)]

investigators = pd.read_csv("script/sql/visualisation/CSV_files/df_investigators.csv")
investigators = investigators[investigators["nct_id"].isin(studies.nct_id)]

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
