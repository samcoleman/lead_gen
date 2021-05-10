import requests
import time
import logging
import sys
import os
from utils.data import TableManger
from utils.const import __CUR_DIR__
import pandas as pd

class Logger:
    def __init__(self):
        # Initiating the logger object
        self.logger = logging.getLogger(__name__)
        
        # Set the level of the logger. This is SUPER USEFUL since it enables you to decide what to save in the logs file.
        # Explanation regarding the logger levels can be found here - https://docs.python.org/3/howto/logging.html
        self.logger.setLevel(logging.DEBUG)
        
        # Create the logs.log file
        handler = logging.FileHandler('nlogs.log')

        # Format the logs structure so that every line would include the time, name, level name and log message
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        
        # Adding the format handler
        self.logger.addHandler(handler)
        
        # And printing the logs to the console as well
        self.logger.addHandler(logging.StreamHandler(sys.stdout))


class Request:
  logger = Logger().logger
  req = requests.Session()
  last_request = time.time()

  request_delay = 3 #s


  @staticmethod        
  def get(html, tries=0):
    try:
      curtime = time.time()
      dt = curtime-Request.last_request
      
      
      if dt < Request.request_delay:
        time.sleep(Request.request_delay-dt)
      
      s = Request.req.get(html, timeout=5)
      Request.last_request = time.time()
      return s
    except requests.exceptions.RequestException as err:
      Request.logger.debug("Connection Error to:"+html+", Error:"+str(err))

      if tries < 50:
          Request.logger.debug("Attempt:"+str(tries+1))
          return Request.get(html,tries+1)
      else:
          Request.logger.debug("Something v wrong??")
          return False
  
  def close(self):
      self.req.close()


class GoogleAPIRequest(object):
  session_request_limit = 5000
  requests_made = 0
  

  api_file = open("api\API_KEY.txt", "r")
  api_key = api_file.read()

  places_search_log = TableManger(os.path.join(__CUR_DIR__, "logs\places_search_log.csv"))

  

  @staticmethod
  def request(url: str):
    if GoogleAPIRequest.requests_made >= GoogleAPIRequest.session_request_limit:
      print("Reached session request limit")
      return {}


    r = Request.get(url + "&key=" + GoogleAPIRequest.api_key).json()
    GoogleAPIRequest.last_request = time.time()

    GoogleAPIRequest.requests_made = GoogleAPIRequest.requests_made + 1

    print("Requests Made: " + str(GoogleAPIRequest.requests_made))

    return r

  @staticmethod
  def places_search(search_str: str):

    if GoogleAPIRequest.places_search_log.check_duplicate('Search String', search_str):
      print("Search: " + search_str + " already complete")
      return

    results = []

    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    rj = GoogleAPIRequest.request(base_url + "query=" + search_str + "&region=uk&fields=name,place_id")

    def next_page(next_page_token, tries = 0):
      # Recursion limit
      if tries > 5:
        return

      rj = GoogleAPIRequest.request(base_url + "pagetoken=" + next_page_token)

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

      # This recursively goes to the next page
      next_page(rj["next_page_token"])
    
    print("Search String: "+ search_str + ", Results found: " + str(len(results)))

    d = {'Search String': search_str, 'Results': [results]}
    df = pd.DataFrame(d)
    GoogleAPIRequest.places_search_log.append_df(df)
    return results





