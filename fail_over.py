import requests
import json
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime as dt
import time
import os
import boto3
from boto3.s3.transfer import S3Transfer
import logging
import pandas as pd
import sys

class PaRappaTheWrappa:

  def __init__(self, state, edate, number_calls, test=False):
      clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
      print "You are using this program because something very bad has happened, please contact your sysadmin immediately. Best of luck."
      time.sleep(10)
      while number_calls > 0:
          clear()
          logging.captureWarnings(True)
          self.edate = edate
          self.state = state
          self.test = test
          print "Requesting from AP API"
          results = self.send_request()
          results_ru = self.get_reporting_unit_level(results)
          ap_results = self.create_file(results_ru)
          print "AP Results returned"
          self.save_tos3(ap_results)
          print "AP Results saved to S3"
          number_calls -= 1
          print "{} calls remaining in this session.".format(number_calls)
          print "Time until next call:"
          if number_calls >0:
            for i in xrange(10,0,-1):
                time.sleep(1)
                sys.stdout.write(str(i)+' ')
                sys.stdout.flush()
          else:
            print "All calls in this session have been completed."
            break

  def send_request(self):
      try:
          response = requests.get(
              url="https://api.ap.org/v2/elections/{}".format(self.edate),
              params={
                  "apiKey": "RfvlGfRM69HT4FqUrGBctEBpRbCANTsV",
                  "statePostal": self.state,
                  "officeID": "P",
                  "level": "RU",
                  "party": "GOP",
                  "format": "json",
                  "test": self.test
              }
          )
          print('Response HTTP Status Code: {status_code}'.format(
              status_code=response.status_code))
          json_data = json.loads(response.content)
          return json_data
      except requests.exceptions.RequestException:
          print('HTTP Request failed')

  def get_reporting_unit_level(self,json_data):
      json_ru = json_data['races'][0]['reportingUnits']
      json_ru.pop(0)

      return json_ru

  def create_file(self, json_ru):
      filename = 'ap_feed_{}_{}.csv'.format(self.state,dt.now().strftime("%Y%m%d%H%M%S"))
      f = open(filename, 'wb+')
      results = csv.writer(f)

      results.writerow(['reportingunitName',
                        'fipsCode',
                        'precinctsTotal',
                        'precinctsReporting',
                        'candidateLast',
                        'voteCount'
                    ])

      for ru in json_ru:
        candidates = ru['candidates']
        for candidate in candidates:
          results.writerow([ru["reportingunitName"],
                            ru["fipsCode"],
                            ru["precinctsTotal"],
                            ru["precinctsReporting"],
                            candidate["last"],
                            candidate["voteCount"]
                        ])

      f.close()
      return filename

  def save_tos3(self,filename):
    s3 = boto3.client('s3')
    transfer = S3Transfer(s3)
    transfer.upload_file(filename,
                        'election-day-backup',
                        filename
                       )
    os.remove(filename)
