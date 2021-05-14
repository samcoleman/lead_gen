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


print("1. Choose business directory name")
bus_dir_file = require_input("Do not put file extension, Recommend -> bus_dir:data\\london_bus_dir",
                             "bus_dir:", lambda inp : True)

bus_dir = TableManger(os.path.join(__CUR_DIR__, bus_dir_file))

print("\n2. Set GoogleAPI request limit")
request_limit = require_input("Recommend -> session_requests:4000", "session_requests:", is_integer)
GoogleAPI.session_request_limit = int(request_limit)

print("\n3. GoogleAPI Places Search")

skip_places = require_input("Recommend -> Skip? [y/n]:n", "Skip? [y/n]:", yes_or_no)

area_tab = None
key = None

if skip_places == "n":
    area_table_file = require_input("Must contain column called 'Location String' which it will use for the search, Recommend -> area_file:areas\\london", "area_file:", file_exists)
    area_tab = TableManger(os.path.join(__CUR_DIR__, area_table_file))

    print("Change search keyword from 'Eyelashes'?")
    change_key = require_input("Recommend -> [y/n]:n", "Change keyword from 'Eyelashes'? [y/n]:", yes_or_no)

    if change_key == "n":
        key = "Eyelashes"

    else:
        key = input("Enter keyword:")

print("\n4. GoogleAPI Detailed Search")
skip_detailed = require_input("Recommend -> Skip? [y/n]:n", "Skip? [y/n]:", yes_or_no)

print("\n5. Webscrape")
skip_scrape = require_input("Recommend -> Skip? [y/n]:n", "Skip? [y/n]:", yes_or_no)


if skip_places == "n":
    places_search(area_tab, key, bus_dir)

if skip_detailed == "n":
    detailed_search(bus_dir)

if skip_scrape == "n":
    webscrape(bus_dir)

export(bus_dir)

