loading = False

black_list = ["NCT03542279", "NCT03993262", "NCT04875975", "NCT04875975", "NCT05198661"]

kw_c1_sub1 = ["Hyperthyroidism", "Hyperhyroid", "Thyrotoxicosis", "Amiodarone-Induced Thyrotoxicosis"]
kw_c1_sub2 = ["Graves disease", "Basedow disease", "autoimmune hyperthyroidism"]
kw_c1_sub3 = ["Graves Ophthalmopathy", "Graves Orbitopathies", "Thyroid eye disease",
              "Thyroid Associated Ophthalmopathies", "Thyroid orbitopathy", "Dysthyroid Ophthalmopathies",
              "Dysthyroid orbitopathy", "Thyroid ophthalmopathy"]

kw_c2_sub1 = ["Hashimoto disease", "Hashimoto", "Lymphocytic thyroiditis", "Chronic lymphocytic thyroiditis ",
              "Chronic thyroiditis", "Autoimmune Thyroiditis", "Thyroiditis, autoimmune", "Thyroiditis autoimmune", "Thyroiditis"]
kw_c2_sub2 = ["Giant cell thyroiditis", "Thyroiditis, subacute", "Subacute thyroiditis", "De Quervain's thyroiditis"]
kw_c2_sub3 = ["Riedel’s thyroiditis", "Postpartum thyroiditis"]

kw_c3_sub1 = ["Thyroid neoplasms", "Thyroid cancer", "Thyroid carcinoma", "Thyroid gland carcinoma", "Thyroid tumor",
              "Neoplasm of Thyroid", "Cancer of the thyroid", "Thyroid Gland Neoplasm", "Carcinoma of the Thyroid",
              "Thyroid neoplasia", "Cancer of thyroid", "Carcinoma of thyroid", "Tumor of the Thyroid",
              "Thyroid gland cancer", "Neoplasm of the Thyroid", "Tumor of Thyroid", "Endocrine Gland Neoplasms",
              "Endocrine tumor", "Endocrine neoplasia", "Endocrine neoplasm", "Neoplasm of the endocrine",
              "thyroid carcinoma, anaplastic"]
kw_c3_sub2 = ["Thyroid cancer, papillary", "papillary thyroid cancer", "papillary thyroid cancer",
              "Papillary thyroid carcinoma", "Thyroid Gland Papillary Carcinoma", "thyroid papillary carcinoma",
              "Papillary Carcinoma Of Thyroid", "Papillary Carcinoma of the Thyroid",
              "Tall cell variant thyroid cancer", "Columnar cell variant thyroid gland papillary carcinoma",
              "Follicular variant thyroid gland papillary carcinoma",
              "Tall cell variant thyroid gland papillary carcinoma"]
kw_c3_sub3 = ["Thyroid cancer, follicular", "Thyroid cancer (follicular cell)", "Follicular thyroid cancer",
              "Thyroid gland follicular carcinoma", "Follicular thyroid cancer lymph node metastasis",
              "Follicular thyroid carcinoma", "adenocarcinoma, follicular", "carcinoma, follicular"]
kw_c3_sub4 = ["Huerthle cell thyroid cancer", "Hurthle cell thyroid cancer", "Thyroid gland hurthle cell carcinoma",
              "Hurthle cell tumor", "Hurthle cell thyroid neoplasia", "Thyroid gland oncocytic follicular carcinoma",
              "Hurthle cell carcinoma of the thyroid"]
kw_c3_sub5 = ["Differentiated Thyroid Cancer"]
kw_c3_sub6 = ["Insular thyroid cancer", "Poorly differentiated thyroid gland carcinoma"]
kw_c3_sub7 = ["Anaplastic thyroid cancer", "Thyroid gland anaplastic carcinoma", "Thyroid cancer, anaplastic",
              "Thyroid carcinoma, anaplastic", "undifferentiated thyroid cancer", "Anaplastic thyroid carcinoma",
              "anaplastic carcinoma of the thyroid"]
kw_c3_sub8 = ["Thyroid gland squamous cell carcinoma"]
kw_c3_sub9 = ["Medullary thyroid cancer", "Medullary thyroid carcinoma", "Thyroid gland medullary carcinoma",
              "Thyroid cancer, medullary"]
kw_c3_sub10 = ["Recurrent thyroid cancer", "Recurrent thyroid tland carcinoma"]
kw_c3_sub11 = ["Metastatic thyroid cancer", "Metastatic thyroid gland carcinoma"]
kw_c3_sub12 = ["Struma", "Struma ovarii"]

kw_c4_sub1 = ["Hyperparathyroidism, primary", "Primary hyperparathyroidism",
              "Hyperparathyroidism, secondary", "Secondary Hyperparathyroidism", "Hyperparathyroidism secondary",
              "Parathyroid diseases", "parathyroid dysfunction", "Disorders of parathyroid gland",
              "Parathyroid Disorders"]
kw_c4_sub2 = ["Parathyroid neoplasms", "Parathyroid tumor"]
kw_c4_sub3 = ["pseudohypoparathyroidism", "pseudopseudohypoparathyroidism"]
kw_c4_sub4 = ["hypoparathyroidism"]
kw_c4_sub5 = ["Hyperparathyroidism"]

kw_c5_sub1 = ["Hypothyroidism", "Hypothyroid", "Low T4"]
kw_c5_sub2 = ["Secondary hypothyroidism ", "Pituitary hypothyroidism", "Central hypothyroidism"]
kw_c5_sub3 = ["Congenital hypothyroidism", "Cretinism", "thyroid dysgenesis"]

kw_c6_sub1 = ["Non Thyroidal Illness Syndrome", "Low T3 syndrome", "Low Triiodothyronine Syndrome", "Euthyroid sick syndrome", "Euthyroid sick syndromes"]

kw_c7_sub1 = ["Goiter", "Goiter, Nodular", "goitre, Nodular",
              "Nodular Goiter", "Nodular goitre", "Multinodular Goiter", "Recurrent Goiter"]

kw_c8_sub1 = ["thyroid nodule", "thyroid gland nodule"]

kw_c9_sub1 = ["Thyroid diseases", "Thyroid disease"]


keys_word_dict = {
    "Hyperthyroidism":
        {
            "Hyperthyroidism": kw_c1_sub1,
            "Graves' disease": kw_c1_sub2,
            "Orbitopathy": kw_c1_sub3
        },
    "Thyroiditis":
        {
            "Hashimoto": kw_c2_sub1,
            "De Quervain's thyroiditis": kw_c2_sub2,
            "Other thyroiditis": kw_c2_sub3
        },
    "Thyroid neoplasms":
        {
            "Thyroid cancer": kw_c3_sub1,
            "Thyroid cancer, papillary": kw_c3_sub2,
            "Thyroid cancer, follicular": kw_c3_sub3,
            "Hurthle cell thyroid cancer": kw_c3_sub4,
            "Differentiated thyroid cancer, all": kw_c3_sub5,
            "Poorly differentiated thyroid cancer": kw_c3_sub6,
            "Thyroid cancer, anaplastic": kw_c3_sub7,
            "Thyroid Gland Squamous Cell Carcinoma": kw_c3_sub8,
            "Thyroid cancer, medullary": kw_c3_sub9,
            "Recurrent Thyroid Cancer": kw_c3_sub10,
            "Metastatic Thyroid Cancer": kw_c3_sub11,
            "Struma ovarii": kw_c3_sub12,
        },
    "Parathyroid diseases":
        {
            "Parathyroid diseases": kw_c4_sub1,
            "Parathyroid cancer": kw_c4_sub2,
            "pseudohypoparathyroidism": kw_c4_sub3,
            "Hypoparathyroidism": kw_c4_sub4,
            "Hyperparathyroidism": kw_c4_sub5
        },
    "Hypothyroidism":
        {
            "Hypothyroidism": kw_c5_sub1,
            "Secondary hypothyroidism": kw_c5_sub2,
            "Congenital hypothyroidism": kw_c5_sub3,
        },
    "Euthyroid Sick Syndromes":
        {
            "Euthyroid Sick Syndromes": kw_c6_sub1
        },
    "Goiter":
        {
            "Goiter": kw_c7_sub1
        },
    "Nodule":
        {
            "Nodule": kw_c8_sub1
        },
    "Non specific thyroid deseases":
        {
            "Non specific thyroid deseases": kw_c9_sub1
        }
}

class_dict = {
    "Industry": ["INDUSTRY", "Ltd.", "Co.", "Inc."],
    "Government Agency": ["NIH", "OTHER_GOV", "VA OFFICE OF RESEARCH AND DEVELOPMENT", "CENTRAL ARKANSAS VETERANS HEALTHCARE SYSTEM" "INCA", "NATIONAL CANCER INSTITUTE", "NATIONAL INSTITUTE"],
    "Health care Institution": ["Health Research Institute", "HOSPITAL", "CANCER CENTER", "MEDICAL CENTER", "CENTRE LEON BERARD", "GUSTAVE ROUSSY", "CHU", "ZIEKENHUIS", "HOPITAUX", "HOSPICES", "OSPEDALIERO", "OSPEDALIERA", "CENTRE FRANCOIS BACLESSE", "MAYO CLINIC", "DANA-FARBER CANCER INSTITUTE"],
    "University": ["UNIVERSITY", "UNIVERSIDAD"],
    "Other organisation": []
}