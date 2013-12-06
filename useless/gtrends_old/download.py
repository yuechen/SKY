from pyGTrends import pyGTrends
import csv, datetime, time, getpass
import re
import sys

google_username = 'skyinvestments99@gmail.com'
google_password = 'gamingthesystem'

def read_csv_data( data ):
    """
        Reads CSV from given path and Return list of dict with Mapping
    """
    csv_reader = csv.reader( data )
    # Read the column names from the first line of the file
    fields = csv_reader.next()
    data_lines = []
    for row in csv_reader:
        items = dict(zip(fields, row))
        data_lines.append(items)
    return data_lines

def getGTData(search_query, date="all", geo="all", scale="1", position="end"):
    connector = pyGTrends(google_username, google_password)
    connector.download_report(search_query, date=date, geo=geo, scale=scale)
    data = connector.csv(section='Main').split('\n')
    csv_reader = csv.reader(data)

    # remove all whitespaces
    search_query = search_query.strip() 
    search_query = " ".join(search_query.split())
    search_query = search_query.replace(" ", "")

    with open( search_query + '_google_report.csv', 'w') as csv_out:
        positionInWeek = { "start" : 0, "end" : 1 }
        separator = " - "
        csv_writer = csv.writer( csv_out )
        #print "LOOPING ON ENTRIES"
        for count, row in enumerate( csv_reader ):
	    if separator not in row[0] : 
                csv_writer.writerow( row )
                continue

            date = row[0].split( separator )[ positionInWeek[ position ] ] 

	    # we want to remove any whitespaces from the value entry since we are not interested in blank data points
            val = re.sub(r'\s+', '', row[1] )
            if len(val) < 1 :
                #print "We will skip Null value at date %s" % str(date)
                continue
            #row = str(date)+','+str(val)
            if count == 0:
                csv_writer.writerow( row )
            else:
                csv_writer.writerow( [ str(date) ] + [ str(val) ])
    print "File saved: %s " % ( search_query + '_google_report.csv' )

def getGoogleTrendData(search_query, date, geo="all", scale="1"):
    getGTData(search_query=search_term, date = date, geo = geo, scale = scale)

if __name__=="__main__":
    search_term = sys.argv[1]
    getGoogleTrendData(search_query=search_term, date="2010-10", geo="US", scale="1" )