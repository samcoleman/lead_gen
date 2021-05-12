from utils.data import *
import os
from utils.const import __CUR_DIR__

from api.googleAPI import GoogleAPI
from api.websiteScrape import WebsiteScrape


file_path = os.path.join(__CUR_DIR__, "areas\London.csv")

concat_area(file_path)
searches = list_search_strings("Eyelashes", file_path)


for search in searches:
  GoogleAPI.places_search(search)


bus_dir = TableManger(os.path.join(__CUR_DIR__, "data\\business_dir.json"))
bus_dir.load_df(".json")
df = bus_dir.get_df()

#df = places_search_to_business_directory()
#df = extract_add_postcode(df)
#df = postcode_to_authcode(df)
#df = authcode_to_income(df)
#df = create_scores(df)

#for index, row in df[0:20].iterrows():
#   GoogleAPI.detailed_search(row['place_id'])

#df = detailed_search_to_business_directory(df)

website_list = df[df['website'] != ""]['website']
print(website_list)

print(len(website_list))

bus_dir.save_df(df, ".json")





#print(WebsiteScrape.scrape("https://www.munasalon.co.uk/"))





