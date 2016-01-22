from api_calls import APICalls
from strategies import ElectionStrategies
from boto_client import BotoClient

class MSReporting:

    def __init__(self, bucket):
        print "Requesting from Microsoft API"
        ms_call = APICalls("MS")
        ms_results = ms_call.ms_results
        election = ElectionStrategies()
        ms_filename = election.ms_processing(ms_results)
        BotoClient(ms_filename, bucket)
        print "Processed and loaded Microsoft Data"
