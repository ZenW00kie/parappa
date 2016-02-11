from datetime import datetime as dt
import pandas as pd
import csv

class ElectionStrategies:

    def __init(self):
        pass

    def ap_init(self,state, results, party):
        no_fips = ["NH"]
        fips = ["IA","SC"]
        self.state = state

        if self.state in no_fips:
            self.fips_process = False
        elif self.state in fips:
            self.fips_process = True
        else:
            pass

        filename= "ap_{}_{}_{}.csv".format(party,state,dt.now().strftime("%Y%m%d%H%M%S"))
        f = open(filename, "wb+")

        if self.fips_process == False:
            self.__nofips_processing(results,f)
        elif self.fips_process == True:
            self.__fips_processing(results,f)
        else:
            pass

        return filename

    def widen_table(self,filename):
        initial_results = pd.read_csv(filename)
        initial_results.sort_values(["reportingunitName","candidateLast"],
                                      inplace=True
                                  )
        wide_results = initial_results.pivot_table(index=["reportingunitName",
                                                          "fipsCode",
                                                          "precinctsTotal",
                                                          "precinctsReporting"
                                                          ],
                                                   columns="candidateLast"
                                                  )
        if self.fips_process == False:
            wide_results["state"] = self.state
        else:
          pass

        wide_results.to_csv("apwide.csv", header = False)


    def ms_processing(self, election_json):
        filename = "ms_IA_{}.csv".format(dt.now().strftime("%Y%m%d%H%M%S"))
        f = open(filename, "wb+")
        results = csv.writer(f)

        results.writerow(["county",
                          "fipscode",
                          "precinct",
                          "candidate",
                          "votes",
                          "isWinner",
                          "WinPercentage"
                      ])

        for precinct in election_json:
          candidates = precinct["Candidates"]

          for candidate in candidates:
            results.writerow([precinct["County"]["Name"],
                              precinct["County"]["FIPSCode"],
                              precinct["Precinct"]["Name"],
                              candidate["Candidate"]["LastName"],
                              candidate.get("Result", 0),
                              candidate.get("IsWinner", False),
                              candidate.get("WinPercentage", 0)
                          ])

        f.close()

        ms_df = pd.read_csv(filename)

        return filename

############################# PRIVATE FUNCTIONS  ###############################
### These functions are used to process data so that Tableau can properly    ###
### map the geographies. For states that have reporting units without FIPS   ###
### they need to have the state abbreviation in the table.                   ###
################################################################################

    def __fips_processing(self, election_json, f):
        results = csv.writer(f)
        results.writerow(["reportingunitName",
                          "fipsCode",
                          "precinctsTotal",
                          "precinctsReporting",
                          "candidateLast",
                          "voteCount"
                      ])

        for ru in election_json:
          candidates = ru["candidates"]
          for candidate in candidates:
            results.writerow([ru["reportingunitName"],
                              ru["fipsCode"],
                              ru["precinctsTotal"],
                              ru["precinctsReporting"],
                              candidate["last"],
                              candidate["voteCount"]
                          ])

        f.close()

    def __nofips_processing(self, election_json, f):
        results = csv.writer(f)
        results.writerow(["reportingunitName",
                          "fipsCode",
                          "precinctsTotal",
                          "precinctsReporting",
                          "candidateLast",
                          "voteCount",
                          "state"
                      ])

        for ru in election_json:
          candidates = ru["candidates"]
          for candidate in candidates:
            results.writerow([ru["reportingunitName"].upper(),
                              ru["fipsCode"],
                              ru["precinctsTotal"],
                              ru["precinctsReporting"],
                              candidate["last"],
                              candidate["voteCount"],
                              self.state
                          ])
        f.close()
