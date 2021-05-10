import pandas as pd
import os


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


class TableManger:
  def __init__(self, file_path: str):
    self.file_path = file_path
    self.df = pd.read_csv(file_path, header=0, index_col=False, sep=",")

  def check_duplicate(self, col_name: str, content: str):
    series = self.df[col_name]

    return content in set(series)

  def overwrite_df(self, df):
    df.to_csv(self.file_path, header=True, index=False, sep=",")

  def append_df(self, df):
    if not os.path.isfile(self.file_path):
        df.to_csv(self.file_path, mode='a', index=False, sep=",")
    else:
        df.to_csv(self.file_path, mode='a', index=False, sep=",", header=False)
