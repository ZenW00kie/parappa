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

  def __init__(self, state, edate, number_calls, db_password, test=False):
      self.edate = edate
      self.state = state
      self.test = test
      self.db_password = db_password
      clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

      while number_calls > 0:
          clear()
          logging.captureWarnings(True)
          print "Requesting from AP API"
          results = self.send_request()
          results_ru = self.get_reporting_unit_level(results)
          ap_results = self.create_file(results_ru)
          print "AP Results returned"
          self.load_apfeed(ap_results)
          self.make_tablewide(ap_results)
          self.save_tos3(ap_results)
          self.load_widetable()
          print "AP Results loaded"
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

      if self.state == 'NH':
          results.writerow(['reportingunitName',
                            'fipsCode',
                            'precinctsTotal',
                            'precinctsReporting',
                            'candidateLast',
                            'voteCount',
                            'state'
                        ])

          for ru in json_ru:
            candidates = ru['candidates']
            for candidate in candidates:
              results.writerow([ru["reportingunitName"].upper(),
                                ru["fipsCode"],
                                ru["precinctsTotal"],
                                ru["precinctsReporting"],
                                candidate["last"],
                                candidate["voteCount"],
                                'NH'
                            ])
      else:
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

  def load_apfeed(self,filename):
      engine = self.connect_sql()
      connect = engine.connect()
      transaction = connect.begin()
      connect.execute('TRUNCATE TABLE {}.reported_votes;'.format(self.state))
      transaction.commit()

      ses = sessionmaker(bind=engine)
      dbcopy_f = open(filename,'r')
      psql_copy = "COPY {}.reported_votes FROM STDIN WITH CSV HEADER".format(self.state)

      conn = engine.raw_connection()
      cur = conn.cursor()
      cur.copy_expert(psql_copy,dbcopy_f)
      conn.commit()
      ses.close_all()

  def make_tablewide(self,filename):

      initial_results = pd.read_csv(filename)
      initial_results.sort_values(['reportingunitName','candidateLast'],
                                    inplace=True
                                )
      wide_results = initial_results.pivot_table(index=['reportingunitName',
                                                        'fipsCode',
                                                        'precinctsTotal',
                                                        'precinctsReporting'
                                                        ],
                                                 columns='candidateLast'
                                                )
      if self.state == 'NH':
          wide_results['state'] = 'NH'
      else:
        pass
      wide_results.to_csv('ap_wide.csv', header = False)

  def load_widetable(self):
      engine = self.connect_sql()
      connect = engine.connect()
      transaction = connect.begin()
      connect.execute('TRUNCATE TABLE {}.reported_x_candidate_votes;'.format(self.state))
      transaction.commit()

      ses = sessionmaker(bind=engine)
      dbcopy_f = open('ap_wide.csv','r')
      psql_copy = "COPY {}.reported_x_candidate_votes FROM STDIN WITH CSV HEADER".format(self.state)

      conn = engine.raw_connection()
      cur = conn.cursor()
      cur.copy_expert(psql_copy,dbcopy_f)
      conn.commit()
      ses.close_all()

      os.remove('ap_wide.csv')

  def save_tos3(self,filename):
    s3 = boto3.client('s3')
    transfer = S3Transfer(s3)
    transfer.upload_file(filename,
                        'election-day',
                        filename
                       )
    os.remove(filename)

  def connect_sql(self):
      engine = create_engine(
                  'postgresql://junto:{}@minas-morgul.cvncnjbhlgez.us-east-1.rds.amazonaws.com:5432/election-day'.format(self.db_password)
              )

      return engine


class MicrosoftElectionFeed:

    def __init__():
        logging.captureWarnings(True)
        clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

        while True:
            clear()
            print "Requesting from Microsoft API"
            results = self.send_request()
            filename = self.create_file(results)
            self.save_tos3(filename)
            print "Microsoft Results saved to S3"
            print "Time until next call:"
            for i in xrange(6,0,-1):
              time.sleep(10)
              sys.stdout.write(str(i)+'s ')
              sys.stdout.flush()

    def send_request(self):
        try:
            response = requests.get(
                url="https://www.iagopcaucuses.com/api/PrecinctCandidateResults"
            )
            print('Response HTTP Status Code: {status_code}'.format(
                status_code=response.status_code))
            json_data = json.loads(response.content)
            json_data = json_data['PrecinctResults']
            return json_data

    except requests.exceptions.RequestException:
        print('HTTP Request failed')

  def create_file(self, json_data):
      filename = 'ms_feed_IA_{}.csv'.format(dt.now().strftime("%Y%m%d%H%M%S"))
      f = open(filename, 'wb+')
      results = csv.writer(f)

      results.writerow(['county',
                        'fipscode',
                        'precinct',
                        'candidate',
                        'votes'
                    ])

      for precinct in json_data:
        candidates = precinct['Candidates']
        for candidate in candidates:
          results.writerow([precinct['County']['Name'],
                            precinct['County']['FIPSCode'],
                            precinct['Precinct']['Name'],
                            candidate["last"],
                            candidate["voteCount"]
                        ])

      f.close()
      return filename


  def save_tos3(self,filename):
    s3 = boto3.client('s3')
    transfer = S3Transfer(s3)
    transfer.upload_file(filename,
                        'election-day',
                        filename
                       )
    os.remove(filename)
