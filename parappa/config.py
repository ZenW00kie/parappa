import argparse

class ConfigPaRappa:
    def __init__(self):
        pass

    def config(self,args=None):
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
                            help = "Boolean for using test results, default is False",
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
