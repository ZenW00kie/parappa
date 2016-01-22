import requests
import json


class APICalls:

    def __init__(self, service, state=None, edate=None, test=None):
        if service == 'AP':
            ap_topline, ap_results = self.__ap_request(state, edate, test)
            return ap_topline, ap_results
        elif service == 'MS':
            ms_results = self.__ms_request()
            return ms_results

############################# PRIVATE FUNCTIONS  ###############################

    def __ap_request(self, state=None, edate=None, test=None):
        try:
            response = requests.get(
                url="https://api.ap.org/v2/elections/{}".format(edate),
                params={
                    "apiKey": "RfvlGfRM69HT4FqUrGBctEBpRbCANTsV",
                    "statePostal": state,
                    "officeID": "P",
                    "level": "RU",
                    "party": "GOP",
                    "format": "json",
                    "test": test
                }
            )
            print('AP Response: {status_code}'.format(
                status_code=response.status_code)

            json_data = json.loads(response.content)
            json_ru = json_data['races'][0]['reportingUnits']
            topline = json_ru.pop(0)

            return (topline, json_ru)

        except requests.exceptions.RequestException:

            print 'AP Request failed'

        #Microsoft only provides results for IA so calls are very simple
    def __ms_request():
        try:
            response = requests.get(
                url="https://www.iagopcaucuses.com/api/PrecinctCandidateResults"
            )

            print('Microsoft Response :{status_code}'.format(
                status_code=response.status_code))

            json_data = json.loads(response.content)
            json_data = json_data['PrecinctResults']

            return json_data

        except requests.exceptions.RequestException:
            print 'Microsoft Request failed'
