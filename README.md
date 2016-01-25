#The Junto Election Night Reporting System

##Intro

This is the election night tracker for the Jeb 2016 campaign, Pa Rappa.
The tracker uses the Associated Press API for its main source of results.
As Microsoft is the official provider of results for the Iowa Caucus, their feed is also collected and processed.
Pa Rappa stores the election results in S3 as transactional files that update every ten seconds to allow for a time series analysis to be done later on reporting precincts.
Pa Rappa also has the ability to write to PostgreSQL so, which is currently being used as the back-end for Tableau visualizations.


##Things you should be aware of

1. Before using Pa Rappa please consult the necessary packages. It is important to set up Boto3 ahead of time using `aws configure` as Pa Rappa will use this to authenticate your access to S3.

2. The AP's most granular reporting level from their API is called a Reporting Unit. These differ for each state and can be from the county to town to precinct level. The data pipeline aspect of this system is indifferent to this. If you would like to change this, you need to edit APICalls.ap_request.

3. The schema used for the visualization for each table that is being written to, has been pregenerated and so the wide transformed table may prove to be picky if the candidates don't line up. Please verify this on the day of the election ahead of results coming in.


##Using Pa Rappa Tha Wrappa

Pa Rappa makes calls to the AP's API for a certain election that the user must specify. The data is then saved in csv format to a S3 bucket within the Junto system called election-day. The data is also loaded into a database in both "long" and "wide" formats for visualization purposes.

The following arguments are made available to you:
  -st STATE, --state STATE [State abbreviation for election to get results.] *
  -D DATE, --date DATE  [Date of election [YYYY-MM-DD]] *
  -c CALLS, --calls CALLS [Number of calls that to make to the API] *
  -t TEST, --test TEST  [Boolean for using test results, default is False]
  -H HOST, --host HOST  [Database host]
  -d DATABASE_NAME, --database_name DATABASE_NAME [Name of the database]
  -u USERNAME, --username USERNAME [Username for the database]
  -P PASSWORD, --password PASSWORD [Password for the database]
  -b BUCKET, --bucket BUCKET [Destination S3 bucket] *

  - * required argument

<sub> Brought to you by Jeb 2016 </sub>
