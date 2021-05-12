
import os

from api.Request import Request
from utils.TableManager import TableManger
from utils.const import __CUR_DIR__
import pandas as pd


class GoogleAPI(object):
  session_request_limit = 3000
  requests_made = 0
  

  api_file = open("api\API_KEY.txt", "r")
  api_key = api_file.read()

  places_search_log = TableManger(os.path.join(__CUR_DIR__, "logs\places_search_log.json"))
  places_search_log.load_df(".json")

  detailed_search_log = TableManger(os.path.join(__CUR_DIR__, "logs\detailed_search_log.json"))
  detailed_search_log.load_df(".json")

  @staticmethod
  def request(url: str):
    if GoogleAPI.requests_made >= GoogleAPI.session_request_limit:
      print("Reached session request limit")
      return {}


    r = Request.get(url + "&key=" + GoogleAPI.api_key, 3).json()

    GoogleAPI.requests_made = GoogleAPI.requests_made + 1

    if (GoogleAPI.requests_made % 20):
      print("Requests Made: " + str(GoogleAPI.requests_made))
    return r

  @staticmethod
  def places_search(search_str: str):

    if GoogleAPI.places_search_log.check_duplicate('Search String', search_str):
      print("Place Search: " + search_str + " already complete")
      return

    results = []

    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    rj = GoogleAPI.request(base_url + "query=" + search_str + "&region=uk&fields=name,place_id")

    def next_page(next_page_token, tries = 0):
      # Recursion limit
      if tries > 5:
        return

      rj = GoogleAPI.request(base_url + "pagetoken=" + next_page_token)

      if (rj["status"] == "INVALID_REQUEST"):
        # This error is thrown if next page is requested before it is ready
        print("Invalid Request")
        
        next_page(next_page_token, tries+1)
      
      if rj != None:
        results.extend(rj["results"])

        # Check if next page key is in response
        if ("next_page_token" in rj):
          next_page(rj["next_page_token"], tries)
        else:
          return
      else:
        return


    if rj != None:
      results.extend(rj["results"])

      if ("next_page_token" in rj):
        # This recursively goes to the next page
        next_page(rj["next_page_token"])
    
    print("Search String: "+ search_str + ", Results found: " + str(len(results)))

    d = {'Search String': search_str, 'Results': [results]}
    df = pd.DataFrame(d)
    GoogleAPI.places_search_log.save_df_append(df, ".json")
    return results

  @staticmethod
  def detailed_search(place_id):

    if GoogleAPI.detailed_search_log.check_duplicate('place_id', place_id):
      print("Place_ID: " + place_id + " already found")
      return None


    base_url = "https://maps.googleapis.com/maps/api/place/details/json?"
    rj = GoogleAPI.request(base_url + "place_id=" + place_id + "&fields=formatted_phone_number,website,url")

    if "result" in rj:
      result = rj["result"]
      d = {'place_id': place_id, 'result': [result]}
      df = pd.DataFrame(d)
      GoogleAPI.detailed_search_log.save_df_append(df, ".json")
      return result
    else:
      print(rj)
      return None









