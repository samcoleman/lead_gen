import pandas as pd
import os

import numpy as np
from utils.TableManager import TableManger
from utils.const import __CUR_DIR__

from api.googleAPI import GoogleAPI



# Create a column called "Location String" which can be used 
def concat_area(file_path:str):
  area_df = pd.read_csv(file_path, header=0, index_col=False, sep=",")
  
  for index, row in area_df.iterrows():
    area_df.at[index, 'Location String'] = row['Location'].lower() + " " + row['Post Town'].split(":")[0].lower()
  
  area_df.to_csv(file_path, header=True, index=False, sep=",")


# Return list of search strings
def list_search_strings(keyword: str, file_path:str):
  area_df = pd.read_csv(file_path, header=0, index_col=False, sep=",")

  search_strings = []

  for index, row in area_df.iterrows():
    search_strings.append(keyword + " in " + row["Location String"])
  
  return search_strings


def places_search_to_business_directory():
  places_search_log = TableManger(os.path.join(__CUR_DIR__, "logs\\places_search_log.json"))
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
  post_area = TableManger(os.path.join(__CUR_DIR__, "data\\postcode_areacode.csv"))
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
  income = TableManger(os.path.join(__CUR_DIR__, "data\\median_income.csv"))
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


def create_scores(df):
  df = TableManger.add_normalised_column(df, "mean_income")
  df = TableManger.add_normalised_column(df, "rating")
  df = TableManger.add_normalised_column(df, "user_ratings_total")

  df["score"] = df["norm_mean_income"] + df["norm_rating"] + df["norm_user_ratings_total"]
  return df


def detailed_search_to_business_directory(df):
  detailed_search_log = TableManger(os.path.join(__CUR_DIR__, "logs\\detailed_search_log.json"))
  detailed_search_log.load_df(".json")

  log_df = detailed_search_log.get_df()

  for index, row in log_df.iterrows():
    print(row)
    bus_dir_row = df[row['place_id']]

    print(bus_dir_row.append(row['result']))

  return log_df







