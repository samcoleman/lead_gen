from utils.data import *
import os
from utils.const import __CUR_DIR__

from api.googleAPI import GoogleAPI


file_path = os.path.join(__CUR_DIR__, "areas\London.csv")

concat_area(file_path)
searches = list_search_strings("Eyelashes", file_path)


for search in searches:
  GoogleAPI.places_search(search)

places_search_to_business_directory()


bus_dir = TableManger(os.path.join(__CUR_DIR__, "data\\business_dir.json"))
bus_dir.load_df(".json")
df = bus_dir.get_df()
print(df['place_id'])

df = extract_add_postcode(df)
df = postcode_to_authcode(df)
df = authcode_to_income(df)
df = create_scores(df)
bus_dir.save_df(df, ".json")


df = df[df['search_results_page'] == 1]

for index, row in df.iloc[0:1].iterrows():
    GoogleAPI.detailed_search(row['place_id'])


print(len(df))









