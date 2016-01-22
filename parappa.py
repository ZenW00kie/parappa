from ap_results import APReporting
from ms_results import MSReporting
import argparse
import sys
import time
import logging
import os

def main():
    #Initializing variables etc
    conf_args = config()
    state = conf_args.state.upper()
    edate = conf_args.date
    number_calls = conf_args.calls
    test = conf_args.test
    host = conf_args.host
    db_name = conf_args.database_name
    db_user = conf_args.username
    db_pword = conf_args.password
    bucket = conf_args.bucket
    clear = lambda: os.system("cls" if os.name == "nt" else "clear")
    ms_newresult = 0
    logging.captureWarnings(True)

    while number_calls > 0:
        APReporting(state, edate, test, db_user, db_pword, host, db_name, bucket)

        if state == "IA" and ms_newresult == 0:
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
        if number_calls >0:
          for i in xrange(10,0,-1):
              time.sleep(1)
              sys.stdout.write(str(i)+" ")
              sys.stdout.flush()

        else:
          print "All calls in this session have been completed."
          break

        clear()

def config(args=None):
    parser = argparse.ArgumentParser(description = "Election Night Result Tracker")
    parser.add_argument("-st", "--state",
                        help = "State abbreviation for election to get results.",
                        required = True,
                        type = str
                        )
    parser.add_argument("-D", "--date",
                        help = "Date of election [YYYY-MM-DD]",
                        required = True,
                        type = str
                        )
    parser.add_argument("-c", "--calls",
                        help = "Number of calls that you would like to make to the API",
                        required = True,
                        type = int
                        )
    parser.add_argument("-t", "--test",
                        help = "Number of calls that you would like to make to the API",
                        required = False,
                        default = False
                        )
    parser.add_argument("-H", "--host",
                        help = "Database host",
                        required = False,
                        default = None
                        )
    parser.add_argument("-d", "--database_name",
                        help = "Name of the database",
                        required = False,
                        default = None
                        )
    parser.add_argument("-u", "--username",
                        help = "Username for the database",
                        required = False,
                        default = None
                        )
    parser.add_argument("-P", "--password",
                        help = "Password for the database",
                        required = False,
                        default = None
                        )
    parser.add_argument("-b", "--bucket",
                        help = "Destination S3 bucket",
                        required = False,
                        default = None
                        )
    arguments = parser.parse_args(args)

    return arguments

if __name__ == "__main__":
    print "Welcome to the Junto Election Night Resuts Tracker. \nPlease make sure that you have configured boto3 using aws configure."
    main()
