from api_calls import APICalls
from strategies import ElectionStrategies
from boto_client import BotoClient

class MSReporting:

    def __init__(self):
        print "Requesting from Microsoft API"
        ms_results = APICalls("MS")
        ms_filename = ElectionStrategies.ms_processing(ms_results)
        BotoClient(ms_filename, bucket)
        print "Processed and loaded Microsoft Data"
