********************************************************************************

# Introduction

********************************************************************************

All credits to the original designer, Sal Uryasev. This is a simple Python Google Trends API that works through parsing the csv file.
The main feature here is the authentication into Google.

Instructions for use can be found at http://www.juiceanalytics.com/openjuice/programmatic-google-trends-api/




********************************************************************************

# What is new in this version?

********************************************************************************

This is an update to the above mentioned pyGTrend.py, it also allows for multiple downloads
in with specific format for use in time series analysis.




********************************************************************************

# Where can I find examples?

********************************************************************************
Here is some basic information using modified pyGTrend.py
example using City to cache search terms

	connector = pyGTrends( google_username, google_password )
	connector.download_report( 
			  		( search_query )
					, date = date
                        		, geo = geo
                        		, scale = scale
				 )

A simple method for writing out the entire entry grabbed from the web
    
	connector.writer( "search_query_name.csv" )

Since the Google Trend data comes in "sections", the code allows one to get different
regions, Main, City and Subregion. The Main section is the time series data where the 
Weeks, Days, Month headers are found. This is often what we use so there is a dedicated
script to dead with grabbing and formatting this.

	data = connector.csv( section='Main' ).split('\n')
	csv_reader = csv.reader( data )


A more detailed example where we output only the "Main" section from the trend result is found
in download.py. The standard format for the date is a range from the start of the week to the end "start - end".
The download.py example will request your gmail login and password from the terminal and
then begin downloading from the list that is specified. In order to parse this more easily
to other programmes the "start" or "end" date is chosen to represent the whoe week.

run via the following command

	./download.py


So until Google decide to change the format once again... Happy trending people!!
