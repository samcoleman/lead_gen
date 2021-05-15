from utils.const import __CUR_DIR__
from utils.Pipeline import *


def require_input(recommend, question, requirement):
    while True:
        print(recommend)
        inp = input(question)

        if requirement(inp) is True:
            break

    return inp

def yes_or_no(inp):
    if inp == "y":
        return True
    elif inp == "n":
        return True
    else:
        print("Input must be 'y' or 'n'")
        return False


def file_exists(inp):
    if not os.path.isfile(os.path.join(__CUR_DIR__, inp+".xlsx")):
        print("File not found")
        return False
    return True

def is_integer(inp):
    try:
        int(inp)
        return True
    except:
        print("Must be an integer")
        return False

# DEFAULTS
bus_dir_file = "data\\london_bus_dir"
area_table_file = "areas\\london"
key = "Eyelashes"
session_limits = 4000


print("Use Defaults")
use_def = require_input("Recommend -> Defaults? [y/n]:y", "Defaults? [y/n]:", yes_or_no)

if use_def == "n":

    print("1. Choose business directory name")
    bus_dir_file = require_input("Do not put file extension, Recommend -> bus_dir:data\\london_bus_dir",
                                 "bus_dir:", lambda inp: True)

    print("\n2. Set GoogleAPI request limit")
    session_limits = require_input("Recommend -> session_requests:4000", "session_requests:", is_integer)


    print("\n3. Choose location input file")
    area_table_file = require_input(
        "Location list, ###.xlsx must contain column called 'Location String' which it will use for the search \nRecommend -> area_file:areas\\london",
        "area_file:", file_exists)

    print("\n4. Choose places search keyword \nUse different search keyword than 'Eyelashes'?")
    change_key = require_input("Recommend -> [y/n]:n", "Change keyword from 'Eyelashes'? [y/n]:", yes_or_no)

    if change_key == "n":
        key = "Eyelashes"
    else:
        key = input("Enter keyword:")


print("\n1. GoogleAPI Places Search")
skip_places = require_input("Recommend -> Skip? [y/n]:n", "Skip? [y/n]:", yes_or_no)

print("\n2. GoogleAPI Detailed Search")
skip_detailed = require_input("Recommend -> Skip? [y/n]:n", "Skip? [y/n]:", yes_or_no)

print("\n3. Webscrape")
skip_scrape = require_input("Recommend -> Skip? [y/n]:n", "Skip? [y/n]:", yes_or_no)


GoogleAPI.session_request_limit = int(session_limits)
bus_dir = TableManger(os.path.join(__CUR_DIR__, bus_dir_file))
area_tab = TableManger(os.path.join(__CUR_DIR__, area_table_file))

if skip_places == "n":
    places_search(area_tab, key, bus_dir, True)
else:
    places_search(area_tab, key, bus_dir, False)

if skip_detailed == "n":
    detailed_search(bus_dir, True)
else:
    detailed_search(bus_dir, False)

if skip_scrape == "n":
    webscrape(bus_dir, True)
else:
    webscrape(bus_dir, False)

export(bus_dir)

