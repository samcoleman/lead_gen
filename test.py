#
# from utils.TableManager import TableManger
# from utils.const import __CUR_DIR__
# import os
#
# scrape_log = TableManger(os.path.join(__CUR_DIR__, "logs\\webscrape_log2.json"))
# scrape_log.load_df(".json")
#
#
# scrape_df = scrape_log.get_df()
# #
#
# count = [d.get('pages') for d in scrape_df.result]
# count = [x+1 for x in count]
#
# print(len(count))
#
# print(scrape_df.loc[1, "result"]["pages"])
# for index, row in scrape_df.iterrows():
#     print(index)
#     scrape_df.at[index, "result"]["pages"] = count[index]
#
# print(scrape_df.iloc[0:10])
#
# scrape_df.drop_duplicates(['base_domain'], inplace=True)
#
# scrape_log.save_df(scrape_df, ".json")