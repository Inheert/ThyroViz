import pandas as pd

articles = pd.read_csv("script/pubmed/data/pubmedArticles.csv", index_col=[0])
articles["Entrez_date"] = pd.to_datetime(articles["Entrez_date"])

publication_type = pd.read_csv("script/pubmed/data/Publication_type.csv", index_col=[0])
all_p_type = [x for x in publication_type.sort_values(by="Publication_type").Publication_type.unique()]

population = pd.read_csv("script/pubmed/data/Population.csv", index_col=[0])
all_population = [x for x in population.sort_values(by="Population").Population.unique()]

full_author_name = pd.read_csv("script/pubmed/data/Full_author_name.csv", index_col=[0]).reset_index(drop=True)
# df = full_author_name.drop_duplicates(subset="Full_author_name")
# all_authors = {df.loc[idx, "Full_author_name"]: df.loc[idx, "Without_special_character"] for idx in df.index}
all_authors = [x for x in full_author_name.sort_values(by="Without_special_character").Without_special_character.unique()]

df_condition = pd.read_csv("script/pubmed/data/Condition.csv", index_col=[0])
all_conditions = [x for x in df_condition.sort_values(by="Category").Category.unique()]

other_term = pd.read_csv("script/pubmed/data/Other_term.csv", index_col=[0])
observational = pd.read_csv("script/pubmed/data/Observational_study_characteristics.csv", index_col=[0])
mesh_term = pd.read_csv("script/pubmed/data/Mesh_terms.csv", index_col=[0])
chemical = pd.read_csv("script/pubmed/data/Chemical.csv", index_col=[0])

card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": "2vmax",
    "margin": "auto",
}
