from api_calls import APICalls
from strategies import ElectionStrategies
from postgres_conn import DatabaseConnector
from boto_client import BotoClient

class APReporting:

    def __init__(self, st, edate, test,party, db_user, db_pword, host, db_name, s3, old_votes, api_key):
        print "Requesting from AP API"
        apapi_call = APICalls("AP", st, edate, test, party, api_key)
        ap_top = apapi_call.ap_topline
        ap_results = apapi_call.ap_results

        if ap_top != None:
            print "Most recent results for ", st
            print "Precincts reporting: ", ap_top["precinctsReportingPct"],"%"
            self.votetotal = 0
            for candidate in ap_top["candidates"]:
                self.votetotal += candidate["voteCount"]

            if self.votetotal == 0:
                for candidate in ap_top["candidates"]:
                    print candidate["last"],": ",candidate["voteCount"],"votes"
            else:
                for candidate in ap_top["candidates"]:
                    print candidate["last"],": ",round((float(candidate["voteCount"])/self.votetotal)*100,2),"% ",candidate["voteCount"],"votes"

            election = ElectionStrategies()
            filename = election.ap_init(st, ap_results,party)

            if host == None:
                pass
            elif old_votes != self.votetotal:
                election.widen_table(filename)
                DatabaseConnector(db_user, db_pword, host, db_name, filename, st)
                DatabaseConnector(db_user, db_pword, host, db_name, "apwide.csv", st)
            else:
                print "No new results to load"

            BotoClient(filename, s3)

            print "AP data processed and loaded"

        else:
            print "Confirm AP has not started streaming results"

    def votecounter(self):
        return self.votetotal
