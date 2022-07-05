from script.pubmed.Pubmed import *


class PubmedGroup:
    directory = f"{os.path.abspath(os.curdir)}/script/pubmed/data"

    col_to_df = ["Full_author_name", "Mesh_terms", "Other_terms", "Publication_type", "Chemical", "Condition",
                 "Observational_study_characteristics"]

    col_to_drop = [x for x in col_to_df]
    col_to_drop.append("Article_identifier")
    col_to_drop.append("Affiliation")

    population_terms = ["child", "infant, newborn", "infant", "child, preschool", "postmenopause", "adolescent",
                        "adult", "young adult", "pregnant women", "middle aged", "aged", "aged, 80 and over",
                        "male", "female"]

    category = {
        "euthyroid sick syndromes": ["euthyroid sick syndromes"],
        "goiter": ["goiter", "goiter, endemic", "goiter, nodular", "goiter, substernal", "lingual goiter"],
        "hyperthyroidism": ["hyperthyroidism", "graves disease", "graves' disease", "graves ophthalmopathy",
                            "thyrotoxicosis", "thyroid crisis"],
        "hyperthyroxinemia": ["hyperthyroxinemia", "hyperthyroxinemia, familial dysalbuminemic",
                              "thyroid hormone resistance syndrome"],
        "hypothyroidism": ["congenital hypothyroidism", "thyroid dysgenesis", "lingual thyroid", "lingual goiter",
                           "hypothyroidism"],
        "thyroid neoplasms": ["thyroid neoplasms", "thyroid cancer, papillary", "thyroid carcinoma, anaplastic"],
        "thyroid nodule": ["thyroid nodule"],
        "thyroiditis": ["thyroiditis, autoimmune", "hashimoto disease", "postpartum thyroiditis",
                        "thyroiditis, subacute", "thyroiditis, suppurative"],
        "thyroid disease": ["thyroid disease"]
    }

    def __init__(self, pathologies: list, filters: list = None, threadingObject: int = 3, delay: float = 1):

        self.dataframes = {}
        self.PubmedObject = [Pubmed(x, filters, delay) for x in pathologies]
        self.threading_list = [threading.Thread(target=obj.RetrieveArticles) for obj in self.PubmedObject]
        self.threadingObject = threadingObject

    def StartRetrieve(self):

        threading_split = []

        count = 0
        thread = []
        for obj in self.threading_list:
            if count < self.threadingObject:
                thread.append(obj)

            elif count == self.threadingObject:
                threading_split.append(thread)
                count = 0
                thread = [obj]
            count += 1

        if len(thread) >= 1:
            threading_split.append(thread)

        print(datetime.now())
        for sub_list in threading_split:
            for obj in sub_list:
                obj.start()
            for obj in sub_list:
                obj.join()
        print(datetime.now())

    def JoinAndCleanDataframe(self):

        final_df = None
        dataframe_list = [df.dataframes for df in self.PubmedObject]

        for df in dataframe_list:
            if final_df is None:
                final_df = df
            final_df = pd.concat([final_df, df])

        self._DataframeSaveAndSplit(final_df, self.col_to_df)

    def _DataframeSaveAndSplit(self, dataframe: pd.DataFrame, new_dataframe: list):

        dataframe = dataframe.reset_index(drop=True)

        self.dataframes["pubmedArticles"] = dataframe

        for column in new_dataframe:

            if column not in self.dataframes["pubmedArticles"]:
                continue

            df = pd.DataFrame(self.dataframes["pubmedArticles"][["PMID", column]].explode(column))
            df = df.drop_duplicates()

            df[column] = df[column].apply(lambda x: None if x == "" else x)
            df = df.dropna()

            if column == "Chemical":
                df[column] = df[column].apply(lambda x: f"{str(x).split('(', maxsplit=1)[1]}" if "(" in x else x)
                df[column] = df[column].apply(lambda x: x.strip(")"))
                df[column] = df[column].apply(
                    lambda x: x.replace("type i", "type 1") if "type i" in x
                    else x.replace("type ii", "type 2") if "type ii" in x
                    else x.replace("type iii", "type 3") if "type iii" in x
                    else x)

            elif column == "Mesh_terms":
                df[column] = df[column].apply(
                    lambda x: x.replace("type i", "type 1") if "type i" in x
                    else x.replace("type ii", "type 2") if "type ii" in x
                    else x.replace("type iii", "type 3") if "type iii" in x
                    else x.replace("class i", "class 1") if "class i" in x
                    else x.replace("class ii", "class 2") if "class ii" in x
                    else x.replace("class iii", "class 3") if "class iii" in x
                    else x)

            elif column == "Condition":
                df["Category"] = df[column].apply(
                    lambda x: self._GetCategoryCondition(x))

            elif column == "Full_author_name":
                df["Without_special_character"] = df[column].apply(lambda x: x.replace(",", ""))

            self.dataframes[column] = df
            self.dataframes[column].to_csv(f"{PubmedGroup.directory}/{column}.csv")

            self._CreateNewDataframes("population", column)

        # self.dataframes["pubmedArticles"] = self.dataframes["pubmedArticles"].drop(columns=[col for col in PubmedGroup.col_to_drop])
        keep = []
        for col in self.dataframes["pubmedArticles"].columns:
            if col not in self.col_to_drop:
                keep.append(col)

        self.dataframes["pubmedArticles"] = self.dataframes["pubmedArticles"].drop_duplicates(subset=keep)
        self.dataframes["pubmedArticles"] = self.dataframes["pubmedArticles"][["PMID", "PII", "DOI", "Title",
                                                                               "Publication_date", "Entrez_date", "Place_of_publication",
                                                                               "Full_journal", "Investigator", "Abstract", "Mesh_terms", "Other_terms",
                                                                               "Chemical"]]
        # dataframe = self.dataframes["pubmedArticles"]
        # dataframe = dataframe[~dataframe.PMID.isin(self.dataframes["Condition"].PMID)]
        # self.dataframes["pubmedArticles"] = dataframe
        self.dataframes["pubmedArticles"].to_csv(f"{PubmedGroup.directory}/pubmedArticles.csv")

    def _CreateNewDataframes(self, newCol, column):
        if newCol == "population" and column == "Mesh_terms":
            df = self.dataframes["Mesh_terms"].copy()

            df["Population"] = df["Mesh_terms"].apply(lambda x: x if x in PubmedGroup.population_terms else None)
            df.dropna(subset="Population", inplace=True)

            self.dataframes["Population"] = df[["PMID", "Population"]]
            self.dataframes["Population"].to_csv(f"{PubmedGroup.directory}/{'Population'}.csv")

    @staticmethod
    def _GetCategoryCondition(pathologie):
        for k, v in Pubmed.category.items():
            if pathologie in v:
                return k

    def GetInfos(self):
        str_pathos = ""
        for pathologie in Pubmed.default_pathologies.keys():
            str_pathos += f", {pathologie}"

        str_filters = ""
        for pubmed_filter in Pubmed.valid_filter:
            str_filters += f", {pubmed_filter}"

        print(f"Total instance: {len(self.threading_list)}")
        print(f"Threading count: {self.threadingObject}")
        print("")
        print(f"Default pathologies: {str_pathos}")
        print(f"available filters: {str_filters}")
