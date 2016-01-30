import requests
import json


class APICalls:

    def __init__(self, service, state=None, edate=None, test=None):
        if service == 'AP':
            self.ap_topline, self.ap_results = self.__ap_request(state, edate, test)
        elif service == 'MS':
            self.ms_topline, self.ms_results = self.__ms_request()

############################# PRIVATE FUNCTIONS  ###############################

    def __ap_request(self, state=None, edate=None, test=None):
        if test == "True":
            request_params={
                "apiKey": "RfvlGfRM69HT4FqUrGBctEBpRbCANTsV",
                "statePostal": state,
                "officeID": "P",
                "level": "RU",
                "party": "GOP",
                "format": "json",
                "test": "True"
            }
        else:
            request_params={
                "apiKey": "RfvlGfRM69HT4FqUrGBctEBpRbCANTsV",
                "statePostal": state,
                "officeID": "P",
                "level": "RU",
                "party": "GOP",
                "format": "json"
            }

        try:
            response = requests.get(
                url="https://api.ap.org/v2/elections/{}".format(edate),
                params = request_params

            )
            print('AP Response: {status_code}'.format(
                status_code=response.status_code))

            json_data = json.loads(response.content)

            if json_data['races'][0].get('reportingUnits', 0) != 0:
                json_ru = json_data['races'][0]['reportingUnits']
                topline = json_ru.pop(0)
                return (topline, json_ru)

            else:
                print 'AP Results have not started streaming.'
                topline = None
                json_ru = None
                return (topline, json_ru)

        except requests.exceptions.RequestException:
            print 'AP Request failed'

    #Microsoft only provides results for IA so calls are very simple
    def __ms_request(self):
        try:
            precinct_level = requests.get(
                url="https://www.iagopcaucuses.com/api/PrecinctCandidateResults", verify=False
            )

            print('Microsoft Response: {status_code}'.format(
                status_code=precinct_level.status_code))

            if precinct_level.status_code == 200:
                json_data = json.loads(precinct_level.content)
                json_data = json_data['PrecinctResults']

                state_level = requests.get(
                    url="https://www.iagopcaucuses.com/api/StateCandidateResults", verify=False
                )

                topline = json.loads(state_level.content)

                return topline, json_data
            else:
                topline = None
                json_data = None
                return topline, json_data

        except requests.exceptions.RequestException:
            print 'Microsoft Request failed'
