# https://www.canva.com/colors/color-palette-generator/
# https://colordesigner.io
# https://colorpicker.fr/#download
# https://getbootstrap.com/docs/4.1/utilities/shadows/
# https://icons.getbootstrap.com/icons/eye-fill/

import psycopg2
import pandas as pd
import copy
from script.ct_const import *
from script.ct_helpers import *
from geopy.geocoders import Nominatim

df = pd.read_csv("script/sql/visualisation/CSV_files/df_investigators.csv")
# Korea, Republic of

geolocator = Nominatim(user_agent="ThyroResearch")

city = "Parker"
country = "United States"
# 35.18850195 128.94497550311712
loc = geolocator.geocode(city+','+country)
print(loc.latitude, loc.longitude)
