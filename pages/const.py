import pandas as pd
from pages.helpers import GetCategoryPercent

studies = pd.read_csv("script/sql/visualisation/CSV_files/studies.csv")
studies["study_first_submitted_date"] = pd.to_datetime(studies["study_first_submitted_date"])

studies_filter = studies = studies[studies["overall_status"].isin(["Recruiting", "Not yet recruiting", "Active, not recruiting"])]

sponsors = pd.read_csv("script/sql/visualisation/CSV_files/df_sponsorsName.csv")
investigators = pd.read_csv("script/sql/visualisation/CSV_files/df_investigators.csv")

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

category = GetCategoryPercent(groupby="category", sortby=["nct_id"], sortasc=False)