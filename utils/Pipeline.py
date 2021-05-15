from api.googleAPI import GoogleAPI
from api.websiteScrape import WebsiteScrape

from utils.data import *
from utils.const import __CUR_DIR__
import openpyxl

a = openpyxl
def places_search(area_table: TableManger, keyword: str, table: TableManger, call_api):

    if call_api is True:
        searches = list_search_strings(keyword, area_table)

        for search in searches:
            GoogleAPI.places_search(search)

        df = places_search_to_business_directory()
    else:
        table.load_df(".json")
        df = table.get_df()
    df = extract_add_postcode(df)
    #df = postcode_to_authcode(df)
    #df = authcode_to_income(df)
    #df = create_scores(df)
    table.save_df(df, ".json")


def detailed_search(table: TableManger, call_api):
    df = table.get_df()

    if call_api is True:
        for index, row in df.iterrows():
           GoogleAPI.detailed_search(row['place_id'])

    df = detailed_search_to_business_directory(df)
    #df = is_chain(df)
    table.save_df(df, ".json")


def webscrape(table: TableManger, call_api):
    df = table.get_df()

    if call_api is True:
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
    print("Export")
    df = table.get_df()
    file_path = table.file_path
    #
    # print(file_path)
    # i = input("aa")
    #
    # writer = pd.ExcelWriter(os.path.join(__CUR_DIR__,"test.xlsx"), engine='openpyxl')
    # df.to_excel(writer, index=False)
    # writer.save()

    table.save_df(df, ".xlsx")
    table.save_df(df[df["advanced_keyword_count"] > 0], ".xlsx", file_path+"_filtered")

# class Pipeline:
#     pipeline = []
#     pipeline_inp = {}
#     input_data = None
#
#     def __init__(self, pipeline, pipeline_inp, datalocation):
#         self.pipeline = pipeline
#         self.pipeline_inp = pipeline_inp



