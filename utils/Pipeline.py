from api.googleAPI import GoogleAPI
from api.websiteScrape import WebsiteScrape

from utils.data import *


def places_search(area_table: TableManger, keyword: str, table: TableManger):
    searches = list_search_strings(keyword, area_table)

    for search in searches:
        GoogleAPI.places_search(search)

    df = places_search_to_business_directory()
    df = extract_add_postcode(df)
    #df = postcode_to_authcode(df)
    #df = authcode_to_income(df)
    #df = create_scores(df)

    table.save_df(df, ".json")


def detailed_search(table: TableManger):
    df = table.get_df()

    for index, row in df.iterrows():
       GoogleAPI.detailed_search(row['place_id'])

    df = detailed_search_to_business_directory(df)
    #df = is_chain(df)
    table.save_df(df, ".json")


def webscrape(table: TableManger):
    df = table.get_df()
    website_list = df[df['website'] != ""]['website'].tolist()

    tot = len(website_list)
    i = 0
    for website in website_list:
      WebsiteScrape.scrape(website)
      print(str(i*100/tot) + "% Complete")
      i = i + 1

    df = webscrape_to_business_directory(df)

    df = cleanup_emails(df)
    df = create_score(df)
    table.save_df(df, ".json")


def export(table: TableManger):
    df = table.get_df()
    table.save_df(df, ".xlsx")

    file_path = table.file_path
    table.save_df(df[df["advanced_keyword_count"] > 0], ".xlsx", file_path+"_filtered")

# class Pipeline:
#     pipeline = []
#     pipeline_inp = {}
#     input_data = None
#
#     def __init__(self, pipeline, pipeline_inp, datalocation):
#         self.pipeline = pipeline
#         self.pipeline_inp = pipeline_inp



