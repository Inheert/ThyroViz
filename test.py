# https://www.canva.com/colors/color-palette-generator/
# https://colordesigner.io
# https://colorpicker.fr/#download
# https://getbootstrap.com/docs/4.1/utilities/shadows/
# https://icons.getbootstrap.com/icons/eye-fill/
from pages.helpers import *

test = GetCategoryPercent()

for x in test.index:
    print(test.loc[x]["nct_id"])
