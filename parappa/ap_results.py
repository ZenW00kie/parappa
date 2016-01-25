from api_calls import APICalls
from strategies import ElectionStrategies
from postgres_conn import DatabaseConnector
from boto_client import BotoClient

class APReporting:

    def __init__(self, st, edate, test, db_user, db_pword, host, db_name, s3):
        print "Requesting from AP API"
        apapi_call = APICalls("AP", st, edate, test)
        ap_topline = apapi_call.ap_topline
        ap_results = apapi_call.ap_results

        print "Most recent results for ", st
        print "Precincts reporting: ", ap_topline["precinctsReportingPct"]

        votetotal = 0
        for candidate in ap_topline["candidates"]:
            votetotal += candidate["voteCount"]

        if votetotal == 0:
            for candidate in ap_topline["candidates"]:
                print candidate["last"],": ",candidate["voteCount"],"votes"
        else:
            for candidate in ap_topline["candidates"]:
                print candidate["last"],": ",round((float(candidate["voteCount"])/votetotal)*100,2),"% ",candidate["voteCount"],"votes"

        election = ElectionStrategies()
        filename = election.ap_init(st, ap_results)

        if host == None:
            pass
        else:
            ElectionStrategies.widen_table(filename)
            DatabaseConnector(db_user, db_pword, host, db_name, filename, st)
            DatabaseConnector(db_user, db_pword, host, db_name, "apwide.csv", st)

        BotoClient(filename, s3)

        print "AP data processed and loaded"
