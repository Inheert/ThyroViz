from pages.helpers import *

test = GetCategoryPercent()

for x in test.index:
    print(test.loc[x]["nct_id"])