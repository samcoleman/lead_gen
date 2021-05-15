import os
import pandas as pd


class TableManger:
  def __init__(self, file_path: str):

    self.file_path = file_path
    self.df = None


  def load_df(self, typ=".csv", **kwargs):
    options = {
      "sep": ",",
      "header": 0,
      "index_col": False,
    }
    options.update(kwargs)

    print("Loading data: " + self.file_path)

    if typ == ".csv":
      self.df = pd.read_csv(self.file_path+".csv", **options)
    elif typ == ".json":
      self.df = pd.read_json(self.file_path+".json", orient='index')
    elif typ == ".xlsx":
      self.df = pd.read_excel(self.file_path+".xlsx", engine='openpyxl', index_col=None)


  def check_duplicate(self, col_name: str, content: str):
    series = self.df[col_name]
    return content in set(series)

  def add_normalised_column(self, df, col_name: str, norm_col_name: str = None):
    if norm_col_name is None:
      norm_col_name = "norm_" + col_name

    df[norm_col_name] = (df[col_name]-df[col_name].min())/(df[col_name].max()-df[col_name].min())
    return df

  @staticmethod
  def get_normalised_column(df, col_name: str):
    return (df[col_name]-df[col_name].min())/(df[col_name].max()-df[col_name].min())

  def get_df(self):
    return self.df

  def save_df(self, df, typ=".csv", file_path=None, **kwargs):

    options = {
      "sep": ",",
      "header": True,
      "index": False
    }
    options.update(**kwargs)

    print("Saving data: " + self.file_path)

    self.df = df
    if file_path is not None:
      self.file_path = file_path

    if typ == ".csv":
      df.to_csv(self.file_path+".csv", **options)
    elif typ == ".json":
      df.to_json(self.file_path+".json", orient='index', indent=2)
    elif typ == ".xlsx":
      writer = pd.ExcelWriter(self.file_path+".xlsx", engine='openpyxl')
      df.to_excel(writer, index=False)
      writer.save()

  def save_df_append(self, df, typ=".csv", file_path=None, **kwargs):

    options = {
      "sep": ",",
      "index": False
    }
    options.update(**kwargs)

    if file_path is not None:
      self.file_path = file_path

    if typ == ".csv":
      if not os.path.isfile(os.path.join(self.file_path, ".csv")):
        df.to_csv(self.file_path+".csv", **options, mode='a')
      else:
        df.to_csv(self.file_path+".csv", **options, mode='a', header=False)
    elif typ == ".json":
      if self.df is None:
        df.to_json(self.file_path+".json", orient='index', indent=2)
        self.df = df
        return

      self.df = pd.concat([self.df, df], ignore_index=True)
      self.df.to_json(self.file_path+".json", orient='index', indent=2)
