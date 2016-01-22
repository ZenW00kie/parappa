#The Junto Election Night Reporting System

##Intro

This system uses the Associated Press API to display results in real time on a Tableau dashboard. For the Iowa Caucuses, Microsoft has been named by the IA GOP as the official data provider and so there is also a feed pulling in from their system. However, this is not visualized in the same place as the AP feed, which will be used as the primary visual source given its history in producing results for previous elections.

##Things you should be aware of

1. The AP's most granular reporting level from their API is called a Reporting Unit. These differ for each state and can be from the county to town to precinct level. The data pipeline aspect of this system is indifferent to this, but anyone planing on doing visualizations utilizing Minas Morgul should refer to the AP about what Reporting Unit is associated with each state.

2. The schema for each table that is being written to, has to be pregenerated and so the wide transformed table may prove to be picky if the candidates don't line up. Please verify this on the day of the election ahead of results coming in.

3. There are redundancy instructions and scripts also here, which have been deployed in a different region in case our primary data center goes offline. Please refer to these for separate instructions on how to deploy this system with the current set-up.


##Using Pa Rappa The Wrappa

Pa Rappa makes calls to the AP's API for a certain election that the user must specify. The data is then saved in csv format to a S3 bucket within the Junto system called election-day. The data is also loaded into a database in both "long" and "wide" formats for visualization purposes.

The following arguments are made available to you:
  - state*: What state you wish to get the results for, in the form of a string using USPS two letter abbreviations
  - edate*: What date the election is being held on, as a string formatted YYYY-MM-DD
  - number_calls*: How many calls you would like to make, calls happen at ten second increments ie 2160 corresponds to 6 hours worth of calls
  - db_password*: The password for Minas Morgul
  - test: Defaults to False, boolean to say if you want test data or real world data

  - * required argument

##Using Microsoft Election Feed

The MS election feed is extremely easy and does not require any arguments. It will make calls every sixty seconds, until the user stops the program. It will write it's data to the same election-day bucket as Pa Rappa.
