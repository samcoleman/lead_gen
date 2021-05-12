import pandas as pd
from utils.const import __CUR_DIR__
import os

df = pd.read_json(os.path.join(__CUR_DIR__, "logs\\places_search_log.json"))


df.to_json(os.path.join(__CUR_DIR__, "logs\\places_search_log2.json"), orient='index', indent=2)