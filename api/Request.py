import time

import requests

from api.Logger import Logger


class Request:
  logger = Logger().logger
  req = requests.Session()
  last_request = time.time()

  @staticmethod
  def get(html, delay=0.5, tries=0):
    try:
      curtime = time.time()
      dt = curtime-Request.last_request


      if dt < delay:
        time.sleep(delay-dt)

      s = Request.req.get(html, timeout=5)
      Request.last_request = time.time()
      return s
    except requests.exceptions.RequestException as err:
      Request.logger.debug("Connection Error to:"+html+", Error:"+str(err))

      if tries < 50:
          Request.logger.debug("Attempt:"+str(tries+1))
          return Request.get(html, delay, tries+1)
      else:
          Request.logger.debug("Something v wrong??")
          return False

  def close(self):
      self.req.close()
