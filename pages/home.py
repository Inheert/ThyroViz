"""
Ajouter la dataframe avec les études par sous catégorie
Réfléchir à une structure de projet pour ne pas encombrer les différentes pages

"""
import dash
from dash import dash_table

import pandas as pd
import dash_bootstrap_components as dbc

from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go

dash.register_page(__name__)

studies = pd.read_csv("script/sql/visualisation/CSV_files/studies.csv")

for col in studies.columns:
    studies[col] = studies[col].apply(lambda x: x.strip() if type(x) == str() else x)

categoryProportion = studies[["category", "nct_id"]]
categoryProportion = categoryProportion.groupby("category").count().reset_index()
categoryProportion["proportion (%)"] = round((categoryProportion["nct_id"] / studies["nct_id"].count()) * 100, 2)
categoryProportion.sort_values(by="proportion (%)", ascending=False, inplace=True)
categoryProportion.rename(columns={"nct_id": "Nombre d'étude"}, inplace=True)

layout = html.Div(
    [
        html.H1(children="Répartition des études par catégorie"),

        dbc.Row(
            [
                dbc.Col(
                    [
                        dash_table.DataTable(categoryProportion.to_dict("records"),
                                             [{"name": i, "id": i} for i in categoryProportion.columns],
                                             row_selectable="single", id="categoryDataframe"),
                    ],
                    width="auto"
                ),
                dbc.Col(
                    [
                        dash_table.DataTable(row_selectable="multi", id="subCategoryDataframe")
                    ],
                    width="auto",
                    style={
                        "overlay": "flex",
                        "flexDirection": "row"
                    }
                ),
            ],
            style={
                "display": "flex",
                "alignItems": "top",
                "justifyContent": "center",
                "horizontalAlign": "center"
            }
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dash_table.DataTable(id="studiesDataframe",
                                             page_size=15)
                    ],
                )
            ],
            style={
                "display": "flex",
                "alignItems": "top",
                "justifyContent": "center",
                "horizontalAlign": "center",
                "marginTop": "15px"
            }
        )

    ]
)


@callback(Output("subCategoryDataframe", "data"),
          Output("subCategoryDataframe", "columns"),
          Output("studiesDataframe", "data"),
          Output("studiesDataframe", "columns"),
          Input("categoryDataframe", "selected_rows"),
          Input("subCategoryDataframe", "selected_rows"))
def subCategoryFilter(row, rows):
    if row is None:
        return None, None, None, None
    row = categoryProportion.iloc[row[0]]["category"]

    df = studies[studies["category"] == row][["nct_id", "sub_category"]]
    count = df["nct_id"].count()
    df = df.groupby("sub_category").count().reset_index()
    df["proportion (%)"] = round((df["nct_id"] / count) * 100, 2)
    df.sort_values(by="proportion (%)", ascending=False, inplace=True)
    df.rename(columns={"nct_id": "nombre d'étude"}, inplace=True)

    if rows is not None:
        sub_category_list = []
        for sub in df.iloc[rows]["sub_category"]:
            sub_category_list.append(sub)

        dff = studies[studies["sub_category"].isin(sub_category_list)][["nct_id", "sub_category", "study_first_submitted_date", "primary_completion_date", "completion_date", "study_type"]]
        return df.to_dict("records"), [{"name": i, "id": i} for i in df.columns], dff.to_dict("records"), [{"name": i, "id": i} for i in dff.columns]

    return df.to_dict("records"), [{"name": i, "id": i} for i in df.columns], None, None
