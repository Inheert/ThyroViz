import script.ct_const
from script.ct_helpers import *
from script.ct_const import *
from script.ct_connection_infos import *
import psycopg2
import pandas as pd
import os
import glob
from datetime import datetime
import copy
import threading

def appLaunch():
    script.ct_const.loading = True

    req1 = threading.Thread(target=AactRequestSQL, args=["global"])
    req2 = threading.Thread(target=AactRequestSQL, args=["non_specific"])

    req1.start()
    req2.start()

    req1.join()
    req2.join()

    path_original = f"{os.path.abspath(os.curdir)}/script/sql"
    path_original = path_original.replace("\\", "/")

    df = pd.read_csv(f"{path_original}/global.csv")
    non_specific = pd.read_csv(f"{path_original}/non_specific.csv")

    nct_id_list = []

    for nct_id in df.nct_id.unique():
        nct_id_list.append(nct_id)

    non_specific = non_specific[~non_specific["nct_id"].isin(nct_id_list)]

    df = pd.concat([df, non_specific])
    df.reset_index(inplace=True)
    df.drop(labels=["index"], axis=1, inplace=True)

    # Valeur par défaut "1" pour les lignes dont la colonne "minimum_age_unit" est égale à "Month"
    df["minimum_age_num"] = [1 if df["minimum_age_unit"][x] == "Month" else df["minimum_age_num"][x] for x in
                             df["minimum_age_unit"].index]

    # Remplissage des valeurs null
    df["minimum_age_num"].fillna(value=0, inplace=True)
    df["maximum_age_num"].fillna(value=120, inplace=True)

    # Création de la colonne "category_age" en concatenant dans un string la colonne "minimum_age_sum" et "maximum_age_sum"
    df["category_age"] = [f"{int(df['minimum_age_num'][x])}-{int(df['maximum_age_num'][x])}" for x in
                          df["minimum_age_unit"].index]

    # Drop des colonnes avec les unités (month/year)
    df = df.drop(axis=1, columns=["minimum_age_unit", "maximum_age_unit"])

    df["category_age"] = df["category_age"].apply(lambda x: CategoryAge(x))

    df["overall_status"] = df["overall_status"].apply(lambda x: x.replace(",", ""))

    # ----------------------------#

    # Copie de la dataframe original pour définir les conditions manquantes
    df_explode = copy.deepcopy(df)
    df_explode = df_explode.drop_duplicates(subset="nct_id", keep="first")

    # Création d'une colonne initalisé en "null", utilisation de la fonction GetAllThyroidConditions()
    df_explode["Thyroid conditions"] = None
    df_explode["Thyroid conditions"] = df_explode["all_conditions"].apply(lambda x: GetAllThyroidConditions(x))

    # Explode de la dataframe + nettoyage et mise en forme de celle-ci
    df_explode = df_explode.explode("Thyroid conditions")
    df_explode = df_explode[df_explode["Thyroid conditions"].notna()]
    df_explode["downcase_mesh_term"] = df_explode["Thyroid conditions"].apply(lambda x: x)

    df = pd.concat([df, df_explode])

    df.drop(labels=["Thyroid conditions"], axis=1, inplace=True)

    df.reset_index(drop=True, inplace=True)

    # ----------------------------#

    # Création des colonnes catégories et sous-catégories vides.
    df[["category", "sub_category"]] = None

    # Boucle sur les sous catégories des catégories du dictionnaire
    for category, sub_category in keys_word_dict.items():

        # boucle sur les listes des sous catégories du dictionnaire
        for sub_key, key_word_list in sub_category.items():
            # Convertion de l'ensemble du texte que possède une liste en minuscule
            key_word_list = list((map(lambda x: x.lower(), key_word_list)))

            # Retourne "category" si le 'downcase_mesh_term' est matché dans la liste de mot clé (key_word_list),
            # si le 'downcase_mesh_term' ne match pas avec la list alors il garde sa valeur d'origine
            df["category"] = [category if df.downcase_mesh_term.iloc[x] in key_word_list else df.category.iloc[x] for x
                              in
                              df["downcase_mesh_term"].index]

            # Même fonctionne qu'au dessus mais pour les sous-catégories.
            df["sub_category"] = [sub_key if df.downcase_mesh_term.iloc[x] in key_word_list else df.sub_category.iloc[x]
                                  for
                                  x in df["downcase_mesh_term"].index]

    # Suppression des lignes dupliquées sur nct_id, category et sous-category
    df.drop_duplicates(subset=["nct_id", "category", "sub_category"], keep="last", inplace=True)

    category_clean_dict = {
        "Thyroid neoplasms": "Thyroid cancer",
        "Hypothyroidism": "Hypothyroidism",
        "Parathyroid diseases": "Parathyroid diseases"
    }

    for k, v in category_clean_dict.items():
        df["useless"] = [True if df.loc[x, "sub_category"] == v and
                                 df[(df["nct_id"] == df.loc[x, "nct_id"]) & (df["category"] == k)].shape[
                                     0] > 1 else False
                         for x in df["nct_id"].index]
        df = df[df["useless"] != True]
        df.drop(columns=["useless"], axis=1, inplace=True)

    for nct_id in df["nct_id"]:
        if nct_id.upper() in list((map(lambda x: x.upper(), black_list))):
            df.drop(df[df.nct_id == nct_id.upper()].index, inplace=True)

    # ----------------------------#

    df["URL"] = None
    df["URL"] = df.nct_id.apply(lambda x: f"https://clinicaltrials.gov/ct2/show/{x}")

    # Création d'un dictionnaire avec l'ensemble des Dataframes qui seront "explode" puis enregistré séparemment de la
    # Dataframe principale

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

        # Reset des index
        df_dict[dataframe].reset_index(drop=True, inplace=True)

        if dataframe == "df_sponsorsName" or dataframe == "df_investigators":
            print(f"[CSV - {dataframe}] Ajout des données...")
            # Générer une requête SQL avec une condition : WHERE (nct_id = * AND name = *)
            condition_list = []
            df_dict[dataframe].drop_duplicates(subset="nct_id", inplace=True)

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
                          FROM {'sponsors' if dataframe == 'df_sponsorsName' else 'facilities'}
                          WHERE LOWER(nct_id) in {text}"""

            cur.execute(request)

            dff = pd.DataFrame(cur.fetchall(), columns=[i[0] for i in cur.description])

            cur.close()
            conn.close()

            if dataframe == "df_sponsorsName":
                # Dictionnaire contenant les infos utile à la classification des sponsors

                dff["new_class"] = None

                dff["new_class"] = dff["id"].apply(lambda x: GetGoodClass(x, dff))
                df_dict[dataframe] = dff
            elif dataframe == "df_investigators":
                dff["continent"] = dff["country"].apply(lambda x: GetContinent(x, 'continent'))
                dff["iso"] = dff["country"].apply(lambda x: GetContinent(x, 'Iso'))
                df_dict[dataframe] = dff

            print(f"[CSV- {dataframe}] Données ajoutées !")

    df_dict["df_country"]["continent"] = df_dict["df_country"]["location"].apply(lambda x: GetContinent(x, "continent"))
    df_dict["df_country"]["iso"] = df_dict["df_country"]["location"].apply(lambda x: GetContinent(x, "Iso"))

    # Chemin d'enregistrement des CSV exploitables ainsi que des backups

    path = f"{path_original}/visualisation"

    if not os.path.isdir(path):
        os.mkdir(path)
        # print("[VISUALISATION] FOLDER CREATED")
    else:
        pass
        # print("[VISUALISATION] FOLDER ALREADY EXIST")

    # Chemin des CSV utilisés pour la visualisation
    path_CSVFiles = f"{path}/CSV_files"

    # Chemin du dossier possédant les backups
    path_backup = f"{path}/CSV_backup"

    # Vérification de l'existance du dossier "CSV_files"
    if not os.path.isdir(path_CSVFiles):
        os.mkdir(path_CSVFiles)
        # print("[DATAFRAME - CSV] FOLDER CREATED")
    else:
        pass
        # print("[DATAFRAME - CSV] FOLDER ALREADY EXIST")

    # Vérification de l'existance du dossier "backup"
    if not os.path.isdir(path_backup):
        os.mkdir(path_backup)
        # print("[DATAFRAME - BACKUP] FOLDER CREATED")
    else:
        pass
        # print("[DATAFRAME - BACKUP] FOLDER ALREADY EXIST\n")

    # Vérificiation de l'existance de .csv dans le dossier CSV_files, si des fichiers existent alors :
    if len(glob.glob(f"{path_CSVFiles}/*.csv")) > 0:

        # Récupération de la date à laquelle le .csv "studies" a été créé
        backup_date = datetime.fromtimestamp(os.path.getmtime(glob.glob(f"{path_CSVFiles}/studies.csv")[0]))
        backup_date = backup_date.strftime("%Y-%m-%d_%H-%M")

        # Création d'un dossier dans backup ayant comme nom la date récupéré au-dessus
        os.mkdir(f"{path_backup}/ClinicalTrials_{backup_date}")

        # Boucle sur l'ensemble des .csv présent dans le dossier CSV_files
        for file in glob.glob(f"{path_CSVFiles}/*.csv"):
            # La variable "file" ressort un chemin (ex : monDossier/CSV_files/studies.csv), la chaine de caractère est
            # split puis le dernier élément est récupéré (studies.csv)
            file = file.replace("\\", "/")
            try:
                file_name = file.split("/")
                file_name = file_name[len(file_name) - 1]
                # Déplacement du csv dans son dossier backup
                os.replace(file, f"{path_backup}/ClinicalTrials_{backup_date}/{file_name}")
                # print(
                #    f"[DATAFRAME - {str(file_name).upper()}] was mooved to backup folder at this date : {backup_date}")
            except:
                pass
                # print(f"error : {file}")

    # Enregistrement du .csv studies dans le dossier "CSV_files"
    df.to_csv(f"{path_CSVFiles}/studies.csv", index=False)
    # print("\n[DATAFRAME - STUDIES] csv have been created")

    # Boucle sur les dataframes du dictionnaire df_dict pour les enregistrer
    for dataframe in df_dict:
        df_dict[dataframe].to_csv(f"{path_CSVFiles}/{dataframe}.csv", index=False)
        print(f"[DATAFRAME - {str(dataframe).upper()}] csv have been created")

    script.ct_const.loading = False
