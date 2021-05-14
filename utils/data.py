import pandas as pd
import os
import sys
import numpy as np
from utils.TableManager import TableManger
from utils.const import __CUR_DIR__
import re
from api.googleAPI import GoogleAPI

# Create a column called "Location String" which can be used 
def concat_area(area_table: TableManger):

  area_table.load_df(".xlsx")
  area_df = area_table.get_df()
  
  for index, row in area_df.iterrows():
    area_df.at[index, 'Location String'] = row['Location'].lower() + " " + row['Post Town'].split(":")[0].lower()

  area_table.save_df(area_df, ".xlsx")


# Return list of search strings
def list_search_strings(keyword: str, area_table: TableManger):
  area_table.load_df(".xlsx")
  area_df = area_table.get_df()

  print(area_df)

  search_strings = []

  for index, row in area_df.iterrows():
    if isinstance(row["Location String"], str):
      search_strings.append(keyword + " in " + row["Location String"])
  
  return search_strings


def places_search_to_business_directory():
  places_search_log = TableManger(os.path.join(__CUR_DIR__, "logs\\places_search_log"))
  places_search_log.load_df(".json")
  log_df = places_search_log.get_df()

  search_df = []
  for index, row in log_df.iterrows():
    df = pd.DataFrame(row['Results'])

    df["search_string"] = row['Search String']

    length = len(df)



    if length <= 20:
      df['search_results_page'] = 1
    elif 40 >= length > 20:
      df.loc[:20, 'search_results_page'] = 1
      df.loc[21:, 'search_results_page'] = 2
    elif length > 40:
      df.loc[:20,   'search_results_page'] = 1
      df.loc[21:40, 'search_results_page'] = 2
      df.loc[41:,   'search_results_page'] = 3

    search_df.append(df)

  total_df = pd.concat(search_df, ignore_index=True)
  total_df.drop_duplicates(subset=["place_id"], inplace=True)
  total_df.drop(columns=['geometry', 'icon', 'opening_hours', 'photos', 'reference', 'types',
                         'permanently_closed', 'plus_code'], inplace=True)

  total_df.set_index('place_id', drop=False, inplace=True)

  return total_df

def extract_add_postcode(df):
  df['postcode'] = df['formatted_address'].str.extract(r'([A-Z]{1,2}[0-9R][0-9A-Z]? [0-9][A-Z]{2})')
  return df

def postcode_to_authcode(df):
  post_area = TableManger(os.path.join(__CUR_DIR__, "data\\postcode_areacode"))
  post_area.load_df(".csv")
  post_area_df = post_area.get_df()
  post_area_df['Postcode 1'] = post_area_df['Postcode 1'].str.replace(' ', '')
  post_area_df['short_pc'] = post_area_df['Postcode 1'].str.replace(' ', '').str[:4]

  lpost_area_df = post_area_df.set_index(['Postcode 1'])
  spost_area_df=  post_area_df.set_index(['short_pc'])

  local_auth_code = []

  for index, row in df.iterrows():
    try:
      lac = lpost_area_df.loc[row['postcode'].replace(' ', '')]['Local Authority Code']
    except:
      if row['postcode'] != np.nan:
        try:
          lac = spost_area_df.loc[row['postcode'][:4].str.replace(' ', '')]['Local Authority Code']
        except:
            lac = None
      else:
        lac = None
    local_auth_code.append(lac)

  df['local_authority_code'] = local_auth_code
  return df

def authcode_to_income(df):
  income = TableManger(os.path.join(__CUR_DIR__, "data\\median_income"))
  income.load_df(".csv", sep="|")
  income_df = income.get_df()

  income_df = income_df.set_index(['Local authority code'])

  mean_incomes = []

  for index, row in df.iterrows():

    try:
      mean_income_str = income_df.loc[row['local_authority_code'].replace(' ', '')]['Total annual income'].str.replace(
        ',', '')
      mean_income = pd.to_numeric(mean_income_str).mean()
    except:
      mean_income = None
    mean_incomes.append(mean_income)

  print(mean_incomes)
  df['mean_income'] = mean_incomes
  return df


# def create_scores(df):
#   df = TableManger.add_normalised_column(df, "mean_income")
#   df = TableManger.add_normalised_column(df, "rating")
#   df = TableManger.add_normalised_column(df, "user_ratings_total")
#
#   df["score"] = df["norm_mean_income"] + df["norm_rating"] + df["norm_user_ratings_total"]
#   return df

def is_chain(df):
  df["chain"] = not df["name"].is_unique


def detailed_search_to_business_directory(df):
  detailed_search_log = TableManger(os.path.join(__CUR_DIR__, "logs\\detailed_search_log"))
  detailed_search_log.load_df(".json")

  log_df = detailed_search_log.get_df()

  df["formatted_phone_number"] = ""
  df["maps_url"] = ""
  df["website"] = ""
  df["facebook"] = np.empty((len(df), 0)).tolist()
  df["instagram"] = np.empty((len(df), 0)).tolist()
  df["twitter"] = np.empty((len(df), 0)).tolist()
  df["linkedin"] = np.empty((len(df), 0)).tolist()

  for index, row in log_df.iterrows():
    try:
      result = row["result"]

      if "formatted_phone_number" in result:
        df.loc[row['place_id'], "formatted_phone_number"] = result["formatted_phone_number"]

      if "url" in result:
        df.loc[row['place_id'], "maps_url"] = result["url"]

      if "website" in result:
        if "facebook" in result["website"]:
          df.loc[row['place_id'], "facebook"].append(result["website"])
        elif "instagram" in result["website"]:
          df.loc[row['place_id'], "instagram"].append(result["website"])
        elif "twitter" in result["website"]:
          df.loc[row['place_id'], "twitter"].append(result["website"])
        elif "linkedin" in result["website"]:
          df.loc[row['place_id'], "linkedin"].append(result["website"])
        else:
          df.loc[row['place_id'], "website"] = result["website"]
    except:
      e = sys.exc_info()[0]
      print("Error: " + str(e))
      continue

  return df


def webscrape_to_business_directory(df):
  scrape_log = TableManger(os.path.join(__CUR_DIR__, "logs\\webscrape_log"))
  scrape_log.load_df(".json")

  scrape_df = scrape_log.get_df()

  scrape_df.drop_duplicates(['base_domain'], inplace=True)

  scrape_df = scrape_df.set_index(['base_domain'])


  df["emails"] = np.empty((len(df), 0)).tolist()
  df["basic_keyword_count"] = 0
  df["advanced_keyword_count"] = 0
  df["price_page"] = ""
  df["scraped_pages"] = 0

  for index, row in df.iterrows():
    domain = row["website"]
    if domain is None:
      continue

    try:
      base_domain = re.findall(r"^.+?[^\/:](?=[?\/]|$)", domain)[0]
    except:
      base_domain = domain

    try:
      result = scrape_df.loc[base_domain]["result"]
    except:
      continue

    row["emails"].extend(result["emails"])
    row["facebook"].extend(result["facebook"])
    row["instagram"].extend(result["instagram"])
    row["twitter"].extend(result["twitter"])
    row["linkedin"].extend(result["linkedin"])

    basic_key_count = 0
    advanced_key_count = 0

    for link in result['keywords']:
      for key in result['keywords'][link]:
        val = result['keywords'][link][key][0]["count"]
        if key == "eyelash" or key == "lash" or key == "extension" or \
                key == "classic" or key == "volume" or key == "russian":
          basic_key_count = basic_key_count + val
        else:
          advanced_key_count = advanced_key_count + val

    df.at[index, "basic_keyword_count"] = basic_key_count
    df.at[index, "advanced_keyword_count"] = advanced_key_count

    most_likely = ""
    freq = 0
    for key in result["prices"]:
      if result["prices"][key]["count"] > freq:
        most_likely = key
        freq = result["prices"][key]["count"]

    df.at[index, "price_page"] = most_likely
    df.at[index, "scraped_pages"] = result["pages"]

  return df


def cleanup_emails(df):
  df["filtered_emails"] = np.empty((len(df), 0)).tolist()

  for index, row in df.iterrows():
    emails = row['emails']

    for email in emails:
      lower_email = email.lower()

      if "wix" in  lower_email:
        continue

      tld_list = [".com", ".co.uk"]

      for tld in tld_list:
        if tld in lower_email:
          res = lower_email[:lower_email.index(tld) + len(tld)]

          res = res.lstrip('0123456789.-')

          row["filtered_emails"].append(res)

  return df


def cleanup_social(df, social):
  df[str("filtered_"+social)] = np.empty((len(df), 0)).tolist()
  filtered_socials = []

  for index, row in df.iterrows():
    socials = row[social]

    for soc in socials:
      lower_soc = soc.lower()

      if social+".com/" in lower_soc:
        filtered_socials.append(soc)

    if len(filtered_socials) > 0:
      row[str("filtered_"+social)].extend(filtered_socials)
    else:
      row[str("filtered_"+social)].extend(row[social])

  return df

def create_score(df):
  norm_rating = TableManger.get_normalised_column(df, "rating")
  norm_user_ratings_total = TableManger.get_normalised_column(df, "user_ratings_total")
  norm_search_page_result = TableManger.get_normalised_column(df, "search_results_page")

  df["advanced_keywords_per_page"] = df["advanced_keyword_count"] / df["scraped_pages"]
  norm_advanced_keywords = TableManger.get_normalised_column(df, "advanced_keywords_per_page")

  df["score"] = norm_rating + norm_user_ratings_total + norm_search_page_result + norm_advanced_keywords

  return df




