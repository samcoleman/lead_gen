
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random
import requests
from urllib.request import urlopen, Request
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import logging
import random
import sys
import json
from itertools import cycle
import time
import random
import datetime

from api.Logger import Logger

import ssl
ssl.match_hostname = lambda cert, hostname: hostname == cert['subjectAltName'][0][1]


class request:
  logger = Logger().logger
  req = requests.Session()
  last_request = time.time()

  current_proxy, current_headers = None, None

  @staticmethod
  def updateproxyheaderpool():
      request.proxypool, request.headerspool = request.create_pools()

      request.current_proxy = next(request.proxypool)
      request.current_headers = next(request.headerspool)

      request.firstproxy = request.current_proxy

      #request.logger.debug("Updating proxy & header pool")
      #request.logger.debug("Starting proxy:" + request.current_proxy)


  @staticmethod
  def get(html, delay=0.5, tries=0):
    if request.current_proxy is None:
        request.updateproxyheaderpool()

    try:
      curtime = time.time()
      dt = curtime - request.last_request


      if dt < delay:
        time.sleep(delay-dt)

      s = request.req.get(html, #proxies={"http": request.current_proxy, "https": request.current_proxy},
           headers=request.current_headers, timeout=30)
      request.last_request = time.time()
      return s
    except requests.exceptions.RequestException as err:
      request.logger.debug("Connection Error to:" + html + ", Error:" + str(err))

      if tries < 15:
          request.logger.debug("Attempt:" + str(tries + 1))
          return request.get(html, delay, tries + 1)
      else:
          request.logger.debug("Something v wrong??")
          return False

  @staticmethod
  def random_header():
      # Create a dict of accept headers for each user-agent.
      accepts = {"Firefox": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                 "Safari, Chrome": "application/xml,application/xhtml+xml,text/html;q=0.9, text/plain;q=0.8,image/png,*/*;q=0.5"}

      # Get a random user-agent. We used Chrome and Firefox user agents.
      # Take a look at fake-useragent project's page to see all other options - https://pypi.org/project/fake-useragent/
      try:
          # Getting a user agent using the fake_useragent package
          ua = UserAgent()
          if random.random() > 0.5:
              random_user_agent = ua.chrome
          else:
              random_user_agent = ua.firefox

      # In case there's a problem with fake-useragent package, we still want the scraper to function
      # so there's a list of user-agents that we created and swap to another user agent.
      # Be aware of the fact that this list should be updated from time to time.
      # List of user agents can be found here - https://developers.whatismybrowser.com/.
      except:

          user_agents = [
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
              "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"]  # Just for case user agents are not extracted from fake-useragent package
          random_user_agent = random.choice(user_agents)

      # Create the headers dict. It's important to match between the user-agent and the accept headers as seen in line 35
      finally:
          valid_accept = accepts['Firefox'] if random_user_agent.find('Firefox') > 0 else accepts['Safari, Chrome']
          headers = {"User-Agent": random_user_agent,
                     "Accept": valid_accept}
      return headers

  @staticmethod
  def proxy_list():
      url = 'https://www.sslproxies.org/'

      # Retrieve the site's page. The 'with'(Python closure) is used here in order to automatically close the session when done
      with requests.Session() as res:
          proxies_page = res.get(url)

      # Create a BeutifulSoup object and find the table element which consists of all proxies
      soup = BeautifulSoup(proxies_page.content, 'html.parser')
      proxies_table = soup.find(id='proxylisttable')

      # Go through all rows in the proxies table and store them in the right format (IP:port) in our proxies list
      proxies = []
      for row in proxies_table.tbody.find_all('tr'):
          if "elite proxy" in row.getText():
              # if "FR" in row.getText():
              proxies.append('{}:{}'.format(row.find_all('td')[0].string, row.find_all('td')[1].string))
          # elif "GB" in row.getText():
          #    proxies.append('{}:{}'.format(row.find_all('td')[0].string, row.find_all('td')[1].string))
          # elif "IE" in row.getText():
          #    proxies.append('{}:{}'.format(row.find_all('td')[0].string, row.find_all('td')[1].string))
          # elif "BE" in row.getText():
          #    proxies.append('{}:{}'.format(row.find_all('td')[0].string, row.find_all('td')[1].string))
      return proxies

  @staticmethod
  # Generate the pools
  def create_pools():
      proxies = request.proxy_list()  # ["51.255.103.170:3129"]
      headers = [request.random_header() for ind in
                 range(len(proxies))]  # list of headers, same length as the proxies list

      # This transforms the list into itertools.cycle object (an iterator) that we can run
      # through using the next() function in lines 16-17.
      proxies_pool = cycle(proxies)
      headers_pool = cycle(headers)
      return proxies_pool, headers_pool

  @staticmethod
  def nextproxy():
      request.current_proxy = next(request.proxypool)
      request.current_headers = next(request.headerspool)

      if request.current_proxy == request.firstproxy:
          request.updateproxyheaderpool()
          return

      request.logger.debug("Now using proxy:" + str(request.current_proxy))

  def close(self):
      self.req.close()
