from script.ct_const import *
import psycopg2
import os
import pandas as pd
from script.ct_connection_infos import *
from geopy.geocoders import Nominatim


# FONCTIONS UTILISES
def AactRequestSQL(request=None, request_source="static", dataframe=None):
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

    cur = conn.cursor()
    print("[SQL] Connexion réussi ! Curseur créé")

    path_original = f"{os.path.abspath(os.curdir)}/script/sql"
    path_original = path_original.replace("\\", "/")

    if not os.path.isdir(path_original):
        os.mkdir(path_original)
        # print("[AACT RETRIEVE] FOLDER HAVE BEEN CREATED")
    else:
        pass
        # print("[AACT RETRIEVE] FOLDER ALREADY EXIST")

    if request_source == "static":

        if request == "global":
            with open(f"{path_original}/global_request", 'r') as file:
                cur.execute(file.read())
        elif request == "non_specific":
            with open(f"{path_original}/non_specific_request", "r") as file:
                cur.execute(file.read())

        request_response = cur.fetchall()

        df = pd.DataFrame(request_response, columns=[i[0] for i in cur.description])
        df.to_csv(f"{path_original}/temp_{request}.csv")

    elif request_source == "dynamic":
        print(f"[CSV - {request}] Ajout des données...")
        # Générer une requête SQL avec une condition : WHERE (nct_id = * AND name = *)
        condition_list = []
        dataframe.drop_duplicates(subset="nct_id", inplace=True)

        for e in dataframe.index:
            condition_list.append(
                f"'{dataframe.nct_id[e].lower()}'")

        text = ""

        for idx, value in enumerate(condition_list):
            text += value
            if idx < len(condition_list) - 1:
                text += ", "

        text = f"({text})"
        sql_request = f"""SELECT *
                      FROM {'sponsors' if request == 'sponsors' else 'facilities'}
                      WHERE LOWER(nct_id) in {text}"""

        if request == "sponsors":
            cur.execute(sql_request)

            df = pd.DataFrame(cur.fetchall(), columns=[i[0] for i in cur.description])

            df["new_class"] = None

            df["new_class"] = df["id"].apply(lambda x: GetGoodClass(x, df))
        elif request == "investigators":
            cur.execute(sql_request)

            df = pd.DataFrame(cur.fetchall(), columns=[i[0] for i in cur.description])

            df["continent"] = df["country"].apply(lambda x: GetGeoInfos(x, 'continent'))
            df["iso"] = df["country"].apply(lambda x: GetGeoInfos(x, 'Iso'))
            df["name"] = df["id"].apply(lambda x: FillNaWithSimilarRow(df, x, "name"))

        df.to_csv(f"{path_original}/temp_{request}.csv")
        print(f"[CSV- {request}] Données ajoutées !")

    cur.close()
    conn.close()
    print("[SQL] Fin de connexion.")


def FillNaWithSimilarRow(df, idx, column):
    row = df[df["id"] == idx]

    return row["city"].iloc[0] if row["name"].iloc[0] is None else row["name"].iloc[0]

# Fonction permettant de transformer les colonnes possédant plusieurs valeurs (colonnes concaténées) en une list pour
# réaliser un "explode" de la colonne
def ColumnTransform(stringChain):
    # Si le format de la chaine de caractère n'est pas un string dans ce cas, on le renvoie tel quel dans la Dataframe
    if type(stringChain) != str:
        return stringChain
    # Dans le cas contraire les "," sont remplacé par une chaine vide, la chaine est convertie en liste via un split
    # du character "|"
    else:
        stringChain = stringChain.split("|")
        return stringChain


# Fonction pour récupérer les continents ou les code Iso des continents
def GetGeoInfos(rowCountry, key):
    # Dictionnaire de pays avec comme valeur le continent et le code Iso
    dico_continent = {'Algeria': {'Continent': 'Africa', 'Iso': 'DZA'},
                      'Argentina': {'Continent': 'South America', 'Iso': 'ARG'},
                      'Australia': {'Continent': 'Pacifica', 'Iso': 'AUS'},
                      'Austria': {'Continent': 'Europe', 'Iso': 'AUT'},
                      'Bangladesh': {'Continent': 'South Asia', 'Iso': 'BGD'},
                      'Belarus': {'Continent': 'North Asia', 'Iso': 'BLR'},
                      'Belgium': {'Continent': 'Europe', 'Iso': 'BEL'},
                      'Brazil': {'Continent': 'South America', 'Iso': 'BRA'},
                      'Bulgaria': {'Continent': 'Europe', 'Iso': 'BGR'},
                      'Burkina Faso': {'Continent': 'Africa', 'Iso': 'BFA'},
                      'Canada': {'Continent': 'North America', 'Iso': 'CAN'},
                      'Chile': {'Continent': 'South America', 'Iso': 'CHL'},
                      'China': {'Continent': 'East Asia', 'Iso': 'CHN'},
                      'Colombia': {'Continent': 'South America', 'Iso': 'COL'},
                      'Costa Rica': {'Continent': 'Central America', 'Iso': 'CRI'},
                      'Croatia': {'Continent': 'Europe', 'Iso': 'HRV'},
                      'Cuba': {'Continent': 'Central America', 'Iso': 'CUB'},
                      'Cyprus': {'Continent': 'Middle East', 'Iso': 'CYP'},
                      'Czech Republic': {'Continent': 'Europe', 'Iso': 'CZE'},
                      'Czechia': {'Continent': 'Europe', 'Iso': 'CZE'},
                      'Denmark': {'Continent': 'Europe', 'Iso': 'DNK'}, 'Egypt': {'Continent': 'Africa', 'Iso': 'EGY'},
                      'England': {'Continent': 'Europe', 'Iso': 'GBR'},
                      'Estonia': {'Continent': 'Europe', 'Iso': 'EST'},
                      'Ethiopia': {'Continent': 'Africa', 'Iso': 'ETH'},
                      'Finland': {'Continent': 'Europe', 'Iso': 'FIN'}, 'France': {'Continent': 'Europe', 'Iso': 'FRA'},
                      'French Guiana': {'Continent': 'South America', 'Iso': 'GUF'},
                      'Georgia (Republic)': {'Continent': 'North Asia', 'Iso': 'GEO'},
                      'Germany': {'Continent': 'Europe', 'Iso': 'DEU'}, 'Ghana': {'Continent': 'Africa', 'Iso': 'GHA'},
                      'Greece': {'Continent': 'Europe', 'Iso': 'GRC'},
                      'Guadeloupe': {'Continent': 'Central America', 'Iso': 'GLP'},
                      'Guam': {'Continent': 'Pacifica', 'Iso': 'GUM'},
                      'Guatemala': {'Continent': 'Central America', 'Iso': 'GTM'},
                      'Haiti': {'Continent': 'Central America', 'Iso': 'HTI'},
                      'Holy See (Vatican City State)': {'Continent': 'Europe', 'Iso': 'VAT'},
                      'Hong Kong': {'Continent': 'East Asia', 'Iso': 'HKG'},
                      'Hungary': {'Continent': 'Europe', 'Iso': 'HUN'},
                      'India': {'Continent': 'South Asia', 'Iso': 'IND'},
                      'Indonesia': {'Continent': 'Southeast Asia', 'Iso': 'IDN'},
                      'Iran': {'Continent': 'Middle East', 'Iso': 'IRN'},
                      'Iran, Islamic Republic of': {'Continent': 'Middle East', 'Iso': 'IRN'},
                      'Ireland': {'Continent': 'Europe', 'Iso': 'IRL'},
                      'Israel': {'Continent': 'Middle East', 'Iso': 'ISR'},
                      'Italy': {'Continent': 'Europe', 'Iso': 'ITA'}, 'Japan': {'Continent': 'East Asia', 'Iso': 'JPN'},
                      'Jordan': {'Continent': 'Middle East', 'Iso': 'JOR'},
                      'Kazakhstan': {'Continent': 'North Asia', 'Iso': 'KAZ'},
                      'Kenya': {'Continent': 'Africa', 'Iso': 'KEN'},
                      'Korea (South)': {'Continent': 'East Asia', 'Iso': 'KOR'},
                      'Korea, Republic of': {'Continent': 'East Asia', 'Iso': 'KOR'},
                      'Kuwait': {'Continent': 'Middle East', 'Iso': 'KWT'},
                      'Latvia': {'Continent': 'Europe', 'Iso': 'LVA'},
                      'Lebanon': {'Continent': 'Middle East', 'Iso': 'LBN'},
                      'Lithuania': {'Continent': 'Europe', 'Iso': 'LTU'},
                      'Macedonia, The Former Yugoslav Republic of': {'Continent': 'Europe', 'Iso': 'MKD'},
                      'Malaysia': {'Continent': 'Southeast Asia', 'Iso': 'MYS'},
                      'Martinique': {'Continent': 'Central America', 'Iso': 'MTQ'},
                      'Mexico': {'Continent': 'North America', 'Iso': 'MEX'},
                      'Monaco': {'Continent': 'Europe', 'Iso': 'MCO'},
                      'Netherlands': {'Continent': 'Europe', 'Iso': 'NLD'},
                      'New Zealand': {'Continent': 'Pacifica', 'Iso': 'NZL'},
                      'Norway': {'Continent': 'Europe', 'Iso': 'NOR'},
                      'Pakistan': {'Continent': 'South Asia', 'Iso': 'PAK'},
                      'Peru': {'Continent': 'South America', 'Iso': 'PER'},
                      'Philippines': {'Continent': 'Southeast Asia', 'Iso': 'PHL'},
                      'Poland': {'Continent': 'Europe', 'Iso': 'POL'},
                      'Portugal': {'Continent': 'Europe', 'Iso': 'PRT'},
                      'Puerto Rico': {'Continent': 'Central America', 'Iso': 'PRI'},
                      'Qatar': {'Continent': 'Middle East', 'Iso': 'QAT'},
                      'Réunion': {'Continent': 'Africa', 'Iso': 'REU'},
                      'Romania': {'Continent': 'Europe', 'Iso': 'ROU'},
                      'Russia (Federation)': {'Continent': 'North Asia', 'Iso': 'RUS'},
                      'Russian Federation': {'Continent': 'North Asia', 'Iso': 'RUS'},
                      'Saudi Arabia': {'Continent': 'Middle East', 'Iso': 'SAU'},
                      'Scotland': {'Continent': 'Europe', 'Iso': 'GBR'},
                      'Serbia': {'Continent': 'Europe', 'Iso': 'SRB'},
                      'Singapore': {'Continent': 'Southeast Asia', 'Iso': 'SGP'},
                      'Slovakia': {'Continent': 'Europe', 'Iso': 'SVK'},
                      'Slovenia': {'Continent': 'Europe', 'Iso': 'SVN'},
                      'South Africa': {'Continent': 'Africa', 'Iso': 'ZAF'},
                      'Spain': {'Continent': 'Europe', 'Iso': 'ESP'},
                      'Sri Lanka': {'Continent': 'South Asia', 'Iso': 'LKA'},
                      'Sweden': {'Continent': 'Europe', 'Iso': 'SWE'},
                      'Switzerland': {'Continent': 'Europe', 'Iso': 'CHE'},
                      'Taiwan': {'Continent': 'East Asia', 'Iso': 'TWN'},
                      'Thailand': {'Continent': 'Southeast Asia', 'Iso': 'THA'},
                      'Tunisia': {'Continent': 'Africa', 'Iso': 'TUN'},
                      'Turkey': {'Continent': 'Middle East', 'Iso': 'TUR'},
                      'Uganda': {'Continent': 'Africa', 'Iso': 'UGA'}, 'Ukraine': {'Continent': 'Europe', 'Iso': 'UKR'},
                      'United Arab Emirates': {'Continent': 'Middle East', 'Iso': 'ARE'},
                      'United Kingdom': {'Continent': 'Europe', 'Iso': 'GBR'},
                      'United States': {'Continent': 'North America', 'Iso': 'USA'},
                      'Uzbekistan': {'Continent': 'North Asia', 'Iso': 'UZB'},
                      'Venezuela': {'Continent': 'South America', 'Iso': 'VEN'}}

    # Condition pour retirer un element en particulier du dictionnaire
    if key.lower() == "continent":

        if rowCountry in dico_continent:
            return dico_continent[rowCountry]["Continent"]

        else:
            return None

    elif key.lower() == "iso":
        if rowCountry in dico_continent:
            return dico_continent[rowCountry]["Iso"]

    elif key.lower() == "geo":
        rowCountry = rowCountry.replace("Korea, Republic of", "Republic of Korea").replace("D.F.", "DF").replace("Ã©",
                                                                                                                 "é").replace(
            "Dist", "District")
        rowCountry = rowCountry.split(" ")[0] if "cedex" in rowCountry.lower() else rowCountry

        geolocator = Nominatim(user_agent="ThyroResearch", timeout=3)

        loc = geolocator.geocode(rowCountry)
        return [loc.latitude, loc.longitude]


# Fonction retournant un string concatenant les différentes tranches d'âge par étude
def CategoryAge(categoryRange):
    returnString = ""

    # Dictionnaire contenant en valeur des listes non génériques
    range_dictionary = {
        "firstRange": [range(0, 18), False, "[0-17]"],
        "secondRange": [range(18, 65), False, "[18-65]"],
        "thirdRange": [range(65, 121), False, "[65 and more]"]
    }

    categoryRange = categoryRange.split("-")

    # Passage en "True" des booléens présents dans le dictionnaire si le range est respecté
    for rang in categoryRange:
        rang = int(rang)
        if rang in range_dictionary["firstRange"][0]:
            range_dictionary["firstRange"][1] = True

        if rang in range_dictionary["secondRange"][0]:
            range_dictionary["secondRange"][1] = True

        if rang in range_dictionary["thirdRange"][0]:
            range_dictionary["thirdRange"][1] = True

    if range_dictionary["firstRange"][1] and range_dictionary["thirdRange"][1]:
        range_dictionary["secondRange"][1] = True

    # Création de la chaine de caractère finale (chaine concaténée)
    for key, value in range_dictionary.items():
        if value[1]:
            returnString += value[2] + "|"

    # Le string retourné est un range pour supprimer le dernier caractère "|" afin qu'il ne soit pas reconnu comme un
    # séparateur par un .split() ultérieur
    return returnString[0:-1]


def GetAllThyroidConditions(x):
    good_condition = []
    x = x.strip()
    all_conditions = x.replace("\xa0", " ").lower().split("|")

    for category, sub_category in keys_word_dict.items():
        # boucle sur les listes des sous catégories du dictionnaire
        for sub_key, key_word_list in sub_category.items():
            key_word_list = list((map(lambda y: y.lower().replace("\xa0", " "), key_word_list)))

            for condition in all_conditions:
                if condition in key_word_list:
                    good_condition.append(condition)

    return good_condition


def GetGoodClass(id, df):
    data = df[df["id"] == id]
    if data["new_class"].isnull:
        data = data.iloc[0]

    for k, v in class_dict.items():
        for key_word in v:
            key_word = key_word.lower()
            if key_word in data["name"].lower():
                return k
    return "Other"


"""
    if "university" in data["name"].lower() and "hospital" not in data["name"].lower():
      return "University"
    elif "hospital" in data["name"].lower():
      return "Health care Institution"
    else:
      return data["new_class"]
"""
