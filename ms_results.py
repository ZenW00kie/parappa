from api_calls import APICalls
from strategies import ElectionStrategies
from boto_client import BotoClient
import pandas as pd

class MSReporting:

    def __init__(self, bucket):
        print "Requesting from Microsoft API"
        ms_call = APICalls("MS")
        ms_results = ms_call.ms_results
        ms_topline = ms_call.ms_topline
        print "Most Microsoft recent results for IA"
        print "Precincts reporting: ", round((ms_topline['PrecinctsReporting']/ms_topline['TotalPrecincts'])*100,2)

        for candidate in ms_topline['StateResults']:
            print candidate['Candidate']['LastName'], ": ", round((candidate.get('WinPercentage',0))*100,2), "% ",int(candidate.get('Result',0))

        election = ElectionStrategies()
        ms_filename = election.ms_processing(ms_results)
        BotoClient(ms_filename, bucket)
        print "Processed and loaded Microsoft Data"
