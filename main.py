from utils.data import *
import os 
import pandas as pd
from api.googleAPIRequest import GoogleAPIRequest
from utils.const import __CUR_DIR__


file_path = os.path.join(__CUR_DIR__, "areas\London.csv")

concat_area(file_path)
searches = list_search_strings("Eyelashes", file_path)

for search in searches[0:3]:
  GoogleAPIRequest.places_search(search)




