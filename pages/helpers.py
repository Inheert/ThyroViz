import traceback
import pandas as pd

studies = pd.read_csv("script/sql/visualisation/CSV_files/studies.csv")
studies["study_first_submitted_date"] = pd.to_datetime(studies["study_first_submitted_date"])

sponsors = pd.read_csv("script/sql/visualisation/CSV_files/df_sponsorsName.csv")
investigators = pd.read_csv("script/sql/visualisation/CSV_files/df_investigators.csv")


def GetCategoryPercent(**kwargs):
    name = "GetCategoryPercent()"

    settings = {
        "columns": ["nct_id", "category"],
        "categoryfilter": None,
        "groupby": None,
        "sortby": [],
        "sortasc": True,
        "divisionby": "all"
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
                print(k)
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

    df = studies[settings["columns"]]
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
