from utils.data import *
import os
from utils.const import __CUR_DIR__
from utils.Pipeline import *
from api.googleAPI import GoogleAPI
from api.websiteScrape import WebsiteScrape


file_path = os.path.join(__CUR_DIR__, "areas\London.csv")
bus_dir = TableManger(os.path.join(__CUR_DIR__, "data\\business_dir.json"))

places_search(file_path, "Eyelashes", bus_dir)

detailed_search(bus_dir)

webscrape(bus_dir)

export(bus_dir)

