import traceback
import pandas as pd
import plotly.graph_objects as go
from pages.const import *


def csvFilter(study_type):

    df = studies

    if study_type:
        df = df[df["study_type"].isin(["Not yet recruiting", "Active, not recruiting", "Recruiting"])]
    return df


def GetCategoryPercent(**kwargs):
    name = "GetCategoryPercent()"

    settings = {
        "columns": ["nct_id", "category"],
        "categoryfilter": None,
        "groupby": None,
        "sortby": [],
        "sortasc": True,
        "divisionby": "all",
        "type_filter": True
    }

    """
    Boucle dans la listes des arguments clés donnés, le nom et le type des clés est vérifiés pour éviter une possible
    erreur dans la suite de la fonction
    """
    _kwargs = [k for k in settings]

    try:
        for k, v in kwargs.items():
            if k not in _kwargs:
                raise KeyError
            elif type(settings[k]) != type(v) and settings[k] is not None:
                raise TypeError

            if type(settings[k]) == list:
                for vv in v:
                    if vv not in settings[k]:
                        settings[k].append(vv)
            else:
                settings[k] = v

    except KeyError:
        print(f"\nKeyError: the argument '{k}' does not exist.")
        print(f"Did you mean '{ArgumentSuggestion(settings, k)}'?")
        print("here is a list of available arguments for the 'GetCategoryPercent()' function:")
        print(_kwargs)
        print("\n")
        return None

    except TypeError:
        print(f"TypeError: The type of the given argument ({type(v)}) is not the one "
              f"requested (expected: {type(settings[k])})")
        print(f"Argument: '{k}'")
        print(f"Function: '{name}'")
        return None

    df = studies.copy()

    if settings["type_filter"]:
        df = df[df["overall_status"].isin(["Recruiting", "Not yet recruiting", "Active, not recruiting"])]

    df = df[settings["columns"]]

    if settings["categoryfilter"] is not None:
        df = df[df["category"].isin([settings["categoryfilter"]])]
    else:
        pass

    if settings["divisionby"] == "all":
        division = studies.shape[0]
    elif settings["divisionby"] == "selection":
        division = df.shape[0]

    df = df.groupby(settings["groupby"]).count().reset_index().sort_values(by=settings["sortby"], ascending=settings["sortasc"])
    df.reset_index(drop=True, inplace=True)
    df["nct_id"] = round((df["nct_id"] / division) * 100, 2)
    df["percent"] = df["nct_id"].apply(lambda x: f"{x}%")

    return df


def ArgumentSuggestion(funcArg, calledArg):

    count = {}

    for k in funcArg:
        count[k] = 0
        for letter in calledArg:
            if letter in k:
                count[k] += 1
    return max(count, key=count.get)


def StudiesByYear(category):
    df = s_base.copy()

    if category != ".":
        df = df[df["category"] == category]

    new_studies_by_year = df[["nct_id", "study_first_submitted_date"]].copy()
    new_studies_by_year["year"] = new_studies_by_year["study_first_submitted_date"].apply(lambda x: x.year)
    new_studies_by_year.drop(columns="study_first_submitted_date", inplace=True)
    new_studies_by_year = new_studies_by_year.groupby("year").count().reset_index().sort_values(by="year")
    new_studies_by_year["year"] = new_studies_by_year["year"].apply(lambda x: int(x))
    new_studies_by_year = new_studies_by_year[new_studies_by_year["year"] >= 1999]

    completed_studies_by_year = df[["nct_id", "completion_date"]].copy()
    completed_studies_by_year["year"] = completed_studies_by_year["completion_date"].apply(lambda x: x.year)
    completed_studies_by_year.drop(columns="completion_date", inplace=True)
    completed_studies_by_year = completed_studies_by_year.groupby("year").count().reset_index().sort_values(by="year")
    completed_studies_by_year["year"] = completed_studies_by_year["year"].apply(lambda x: int(x))
    completed_studies_by_year = completed_studies_by_year[
        (completed_studies_by_year["year"] <= datetime.now().year) & (completed_studies_by_year["year"] >= 1999)]

    trace0 = go.Scatter(x=new_studies_by_year["year"], y=new_studies_by_year["nct_id"], mode="lines+text",
                        text=new_studies_by_year["nct_id"], textposition="top center")
    trace1 = go.Scatter(x=completed_studies_by_year["year"], y=completed_studies_by_year["nct_id"], mode="lines+text",
                        text=completed_studies_by_year["nct_id"], textposition="bottom center")

    data = [trace0, trace1]

    return data


def GetSubCategoryProportion(category, s_type, age=None):

    color_pie = ["hsl(201.22, 95.82%, 53.14%)",
                 "hsl(216.05, 100%, 55.29%)",
                 "hsl(230.67, 98.25%, 55.1%)",
                 "hsl(243.98, 100%, 55.69%)",
                 "hsl(244.41, 100%, 86.67%)",
                 "hsl(258.18, 78.2%, 58.63%)",
                 "hsl(258, 77.78%, 35.29%)",
                 "hsl(293.5, 77.34%, 39.8%)",
                 "hsl(293.62, 77.05%, 11.96%)",
                 "hsl(264.1, 96.83%, 50.59%)",
                 "hsl(185.23, 100%, 52.75%)",
                 "hsl(264.44, 96.43%, 89.02%)"]

    df = s_base[["nct_id", "category", "sub_category", "study_type", "minimum_age_num", "maximum_age_num"]].copy()

    if age is not None:
        df = df[(df["minimum_age_num"] >= age[0]) & (df["maximum_age_num"] <= age[1])]

    color_dict = {}

    if category == ".":
        idx = 0
        for cat in df.category.sort_values().unique():
            color_dict[cat] = color_pie[idx]
            idx += 1
        if s_type is None:
            df = df.groupby("category").count().reset_index().sort_values(by="nct_id", ascending=False)
            df.rename(columns={"category": "view"}, inplace=True)
        else:
            df = df[df["study_type"] == s_type]
            df = df.groupby("category").count().reset_index().sort_values(by="nct_id", ascending=False)
            df.rename(columns={"category": "view"}, inplace=True)
        df["color"] = df["view"].apply(lambda x: color_dict[x])

    else:
        for cat in df.category.sort_values().unique():
            idx = 0
            for sub in df[df["category"] == cat]["sub_category"].unique():
                color_dict[sub] = color_pie[idx]
                idx += 1
        if s_type is None:
            df = df[df["category"] == category]
            df = df.groupby("sub_category").count().reset_index().sort_values(by="nct_id", ascending=False)
            df.rename(columns={"sub_category": "view"}, inplace=True)
        else:
            df = df[(df["category"] == category) & (df["study_type"] == s_type)]
            df = df.groupby("sub_category").count().reset_index().sort_values(by="nct_id", ascending=False)
            df.rename(columns={"sub_category": "view"}, inplace=True)
        df["color"] = df["view"].apply(lambda x: color_dict[x])

    return df


category = GetCategoryPercent(groupby="category", sortby=["nct_id"], sortasc=False)