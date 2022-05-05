# https://www.canva.com/colors/color-palette-generator/
# https://colordesigner.io
# https://colorpicker.fr/#download
# https://getbootstrap.com/docs/4.1/utilities/shadows/
# https://icons.getbootstrap.com/icons/eye-fill/

import psycopg2
import pandas as pd
import copy
from script.ct_const import *
from script.ct_helpers import *

DB_HOST = "aact-db.ctti-clinicaltrials.org"
DB_NAME = "aact"
DB_USER = "theo"
DB_PASS = "ag911qbtlm"

df = pd.read_csv("script/sql/visualisation/CSV_files/studies.csv")

def inv():
    df_dict = {
        "df_sponsorsName": copy.deepcopy(df[["nct_id", "sponsors_name"]]),
        "df_investigators": copy.deepcopy(df[["nct_id", "investigators"]]),
        "df_intervention_types": copy.deepcopy(df[["nct_id", "intervention_types"]]),
        "df_country": copy.deepcopy(df[["nct_id", "location"]]),
        "df_age_range": copy.deepcopy(df[["nct_id", "category_age"]])
    }

    # Boucle sur les dataframes du dictionnaire "df_dict" pour explode et nettoyer la dataframe
    for dataframe in df_dict:
        # Liste des colonnes de la dataframe
        col = df_dict[dataframe].columns

        # Application de la fonction ColumnTransform()
        df_dict[dataframe][col[1]] = df_dict[dataframe][col[1]].apply(lambda x: ColumnTransform(x))

        # Explode de la colonne 1 (correspond à la colonne concaténé)
        df_dict[dataframe] = df_dict[dataframe].explode(col[1])

        df_dict[dataframe].dropna(axis=0, how="any", inplace=True)

        df_dict[dataframe].drop_duplicates(inplace=True)

        df_dict[dataframe].drop_duplicates(subset="nct_id", keep="first", inplace=True)

        # Reset des index
        df_dict[dataframe].reset_index(inplace=True)

        if dataframe == "df_investigators":
            print("start")
            condition_list = []

            for e in df_dict[dataframe].index:
                condition_list.append(
                    f"'{df_dict[dataframe].nct_id[e].lower()}'")

            text = ""

            for idx, value in enumerate(condition_list):
                text += value
                if idx < len(condition_list) - 1:
                    text += ", "

            text = f"({text})"
            print(text)

            conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
            cur = conn.cursor()

            request = f"""
            SELECT * FROM facilities
            WHERE nct_id IN {text}
            """

            cur.execute(request)

            df_investigators = pd.DataFrame(cur.fetchall(), columns=[i[0] for i in cur.description])

            cur.close()
            conn.close()

            df_investigators.to_csv("script/sql/visualisation/investigators.csv")


def spons():
    df_dict = {
        "df_sponsorsName": copy.deepcopy(df[["nct_id", "sponsors_name"]]),
        "df_investigators": copy.deepcopy(df[["nct_id", "investigators"]]),
        "df_intervention_types": copy.deepcopy(df[["nct_id", "intervention_types"]]),
        "df_country": copy.deepcopy(df[["nct_id", "location"]]),
        "df_age_range": copy.deepcopy(df[["nct_id", "category_age"]])
    }

    # Boucle sur les dataframes du dictionnaire "df_dict" pour explode et nettoyer la dataframe
    for dataframe in df_dict:
        # Liste des colonnes de la dataframe
        col = df_dict[dataframe].columns

        # Application de la fonction ColumnTransform()
        df_dict[dataframe][col[1]] = df_dict[dataframe][col[1]].apply(lambda x: ColumnTransform(x))

        # Explode de la colonne 1 (correspond à la colonne concaténé)
        df_dict[dataframe] = df_dict[dataframe].explode(col[1])

        df_dict[dataframe].dropna(axis=0, how="any", inplace=True)

        df_dict[dataframe].drop_duplicates(inplace=True)

        df_dict[dataframe].drop_duplicates(subset="nct_id", keep="first", inplace=True)

        # Reset des index
        df_dict[dataframe].reset_index(drop=True, inplace=True)

        if dataframe == "df_sponsorsName":
            condition_list = []

            sp = df_dict[dataframe]
            print(sp[sp["nct_id"] == "NCT04376203"])

            for e in df_dict[dataframe].index:
                condition_list.append(
                    f"'{df_dict[dataframe].nct_id[e].lower()}'")

            text = ""

            for idx, value in enumerate(condition_list):
                text += value
                if idx < len(condition_list) - 1:
                    text += ", "

            text = f"({text})"

            conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

            cur = conn.cursor()

            request = f"""SELECT *
              FROM sponsors
              WHERE LOWER(nct_id) in {text}"""

            cur.execute(request)

            df_sponsors = pd.DataFrame(cur.fetchall(), columns=[i[0] for i in cur.description])

            cur.close()
            conn.close()

            # Dictionnaire contenant les infos utile à la classification des sponsors

            df_sponsors["new_class"] = None

            df_sponsors["new_class"] = df_sponsors["id"].apply(lambda x: GetGoodClass(x, df_sponsors))
            df_dict[dataframe] = df_sponsors
            df_sponsors.to_csv("script/sql/visualisation/sponsors2.csv")


spons()

dff = pd.read_csv("script/sql/visualisation/sponsors.csv")
dfff = pd.read_csv("script/sql/visualisation/sponsors2.csv")

dffff = dff[~dff["nct_id"].isin(dfff["nct_id"].unique())]
dffff = dffff.drop(labels="Unnamed: 0", axis=1)
print(dffff[["nct_id", "name"]])