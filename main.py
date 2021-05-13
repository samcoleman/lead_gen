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

df = places_search_to_business_directory()
df = extract_add_postcode(df)
#df = postcode_to_authcode(df)
#df = authcode_to_income(df)
#df = create_scores(df)

#for index, row in df[0:20].iterrows():
#   GoogleAPI.detailed_search(row['place_id'])

df = detailed_search_to_business_directory(df)
df = webscrape_to_business_directory(df)

#print(df[df['website'] != ""].iloc[0:5])

#website_list = df[df['website'] != ""]['website'].tolist()

#website_list = [x for x in website_list if x != "http://www.glamourlasheslondon.com/"]
#website_list = [x for x in website_list if x != "https://www.agnesdossantos.com/"]
#website_list = [x for x in website_list if x != "https://www.beckylaroc.co.uk/"]


#tot = len(website_list)
#i = 0
#for website in website_list:
#  WebsiteScrape.scrape(website)
#  print(str(i/tot) + "% Complete")
#  i = i + 1

df.to_excel(os.path.join(__CUR_DIR__, "data\\business_dir.xlsx"), index=False)


print(len(df[df["basic_keyword_count"]>0]))

bus_dir.save_df(df, ".json")





#print(WebsiteScrape.scrape("https://www.munasalon.co.uk/"))





