import pandas as pd
import plotly.graph_objects as go
from pages.utilities.const import *


def csvFilter(study_type):
    df = s_base

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
        "sortasc": False,
        "type_filter": False,
        "drop_duplicates": [],
        "divide": "all",
        "divide_col": ""
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

    df = s_base.copy()

    if len(settings["drop_duplicates"]) > 0:
        df.drop_duplicates(subset=settings["drop_duplicates"], keep="first", inplace=True)

    if settings["type_filter"]:
        df = df[df["overall_status"].isin(["Recruiting", "Not yet recruiting", "Active, not recruiting"])]

    df = df[settings["columns"]]

    if settings["categoryfilter"] is not None:
        df = df[df["category"].isin([settings["categoryfilter"]])]
    else:
        pass

    division = df.nct_id.unique().shape[0] if settings["divide"].lower() == "all" else df[~df[settings["divide_col"]].isnull()].nct_id.unique().shape[0]

    df = df.groupby(settings["groupby"]).count().reset_index().sort_values(by=settings["sortby"],
                                                                           ascending=settings["sortasc"])

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


def StudiesByYear(category, dateColumn, minYear, maxYear, periodDisplay, figure):
    df = s_base.copy()
    df.drop_duplicates(subset="nct_id", keep="first", inplace=True)
    date_limit = ["primary_completion_date", "completion_date"]
    data = []

    if category in all_category:
        df = df[df["category"] == category]

    if dateColumn is None or len(dateColumn) < 1:
        dateColumn = ["study_first_submitted_date"]

    if minYear is None:
        minYear = 1999
    if maxYear is None:
        maxYear = datetime.now().year

    if periodDisplay is None or len(periodDisplay) < 1:
        period = "Y"
    elif periodDisplay[0] == "month":
        period = "M"
    else:
        period = "Y"

    for col in dateColumn:
        dff = df[["nct_id", col]].copy()
        # dff.drop(columns=col, inplace=True)
        dff.set_index(col, inplace=True)

        dff = dff.groupby(pd.Grouper(freq=period)).count().reset_index().sort_values(by=col)
        dff = dff[(dff[col] >= datetime(minYear, 1, 1)) & (dff[col] <= datetime(maxYear, 12, 31))]
        if figure is None or figure.lower() == "line":
            trace = go.Scatter(x=dff[col],
                               y=dff["nct_id"],
                               name=col.replace("_", " "),
                               mode="lines+text",
                               text=dff["nct_id"],
                               textposition="bottom center" if col == "completion_date" else "top center")
        elif figure.lower() == "bar":
            trace = go.Bar(x=dff[col],
                           y=dff["nct_id"],
                           name=col.replace("_", " "),
                           text=dff["nct_id"],
                           textposition="outside")
        data.append(trace)

    return data


def GetSubCategoryProportion(selected, s_type, s_status, ageMin, ageMax):
    if s_type is None:
        s_type = []
    if s_status is None:
        s_status = []

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

    df = s_base[["nct_id", "category", "sub_category", "study_type", "overall_status", "minimum_age_num",
                 "maximum_age_num"]].copy()

    ageMin = ageMin if isinstance(ageMin, int) else 0
    ageMax = ageMax if isinstance(ageMax, int) else 100
    # if age is not None:
    #     age = list((map(lambda x: int(float(x)), age)))
    #     df = df[(df["minimum_age_num"] >= age[0]) & (df["maximum_age_num"] <= age[1])]

    color_dict = {}
    if selected == "." or selected is None:
        idx = 0
        for cat in df.category.sort_values().unique():
            color_dict[cat] = color_pie[idx]
            idx += 1

        df.drop_duplicates(subset=["category", "nct_id"], keep="first", inplace=True)

        if len(s_type) > 0:
            df = df[df["study_type"].isin(s_type if isinstance(s_type, list) else [s_type])]
        if len(s_status) > 0:
            df = df[df["overall_status"].isin(s_status if isinstance(s_status, list) else [s_status])]
        df.rename(columns={"category": "view"}, inplace=True)

    else:
        for cat in df.category.sort_values().unique():
            idx = 0
            for sub in df[df["category"] == cat]["sub_category"].unique():
                color_dict[sub] = color_pie[idx]
                idx += 1

        df = df[df["category"] == selected]

        if len(s_type) > 0:
            df = df[df["study_type"].isin(s_type if isinstance(s_type, list) else [s_type])]
        if len(s_status) > 0:
            df = df[df["overall_status"].isin(s_status if isinstance(s_status, list) else [s_status])]
        df.rename(columns={"sub_category": "view"}, inplace=True)

    if ageMin <= 0 and ageMax < 100:
        df = df[df["maximum_age_num"] <= ageMax]
    elif ageMin > 0 and ageMax >= 100:
        df = df[df["minimum_age_num"] >= ageMin]
    elif ageMin <= 0 and ageMax >= 100:
        pass
    else:
        df = df[(df["minimum_age_num"] >= ageMin) & (df["maximum_age_num"] <= ageMax)]

    df = df.groupby("view").count().reset_index().sort_values(by="nct_id", ascending=False)
    df["color"] = df["view"].apply(lambda x: color_dict[x])
    return df


category = GetCategoryPercent(groupby="category", sortby=["nct_id"], drop_duplicates=["category", "nct_id"])