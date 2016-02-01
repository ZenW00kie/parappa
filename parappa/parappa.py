from ap_results import APReporting
from ms_results import MSReporting
from config import ConfigPaRappa
import sys
import time
import logging
import os

def main():
    #Initializing variables etc
    config = ConfigPaRappa()
    conf_args = config.config()
    state = conf_args.state.upper()
    edate = conf_args.date
    number_calls = conf_args.calls
    test = conf_args.test
    party = conf_args.party
    host = conf_args.host
    db_name = conf_args.database_name
    db_user = conf_args.username
    db_pword = conf_args.password
    bucket = conf_args.bucket
    ms_newresult = 0
    logging.captureWarnings(True)

    clear = lambda: os.system("cls" if os.name == "nt" else "clear")

    while number_calls > 0:
        print "Election Feed for ", state, " on ", edate

        APReporting(state, edate, test, party, db_user, db_pword, host, db_name, bucket)

        if state == "IA" and ms_newresult == 0 and party == 'GOP':
            MSReporting(bucket)
        else:
            pass

        #Make Microsoft calls every minute as that is their refresh rate
        if ms_newresult == 5:
            ms_newresult = 0
        else:
            ms_newresult += 1

        number_calls -= 1

        print "{} calls remaining in this session.".format(number_calls)
        print "Time until next call:"

        #Calls to the AP are made every 10 seconds to avoid overuse
        if number_calls >0 and party == 'GOP':
          for i in xrange(10,-1,-1):
              time.sleep(1)
              sys.stdout.write(str(i)+" ")
              sys.stdout.flush()

        elif number_calls >0 and party == 'Dem':
            for i in xrange(60,-1,-1):
                time.sleep(1)
                sys.stdout.write(str(i)+" ")
                sys.stdout.flush()

        else:
          print "All calls in this session have been completed."
          break

        clear()

if __name__ == "__main__":
    print "Welcome to the Junto Election Night Resuts Tracker."
    print "Please make sure that you have configured boto3 using aws configure."
    main()
