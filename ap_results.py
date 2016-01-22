from api_calls import APICalls
from strategies import ElectionStrategies
from postgres_conn import DatabaseConnector
from boto_client import BotoClient

class APReporting:

    def __init__(self, state, edate, test):
        print "Requesting from AP API"
        ap_topline, ap_results = APICalls("AP", state, edate, test)

        print "Most recent results for ", state
        print "Precincts reporting: ", ap_topline["precinctsReportingPct"]
        print "Bush: ", ap_topline["candidates"]["Bush"], " votes"
        print "Cruz: ", ap_topline["candidates"]["Cruz"], " votes"
        print "Rubio: ", ap_topline["candidates"]["Rubio"], " votes"
        print "Trump: ", ap_topline["candidates"]["Trump"], " votes"
        print "Christie: ", ap_topline["candidates"]["Christie"], " votes"
        print "Kasich: ", ap_topline["candidates"]["Kasich"], " votes"
        print "Carson: ", ap_topline["candidates"]["Carson"], " votes"

        filename = ElectionStrategies.ap_init(state, ap_results)

        if host == None:
            pass
        else:
            ElectionStrategies.widen_table(filename)
            DatabaseConnector(db_user, db_pword, host, db_name, filename, state)
            DatabaseConnector(db_user, db_pword, host, db_name, "apwide.csv", state)

        BotoClient(filename, bucket)

        print "AP data processed and loaded"
