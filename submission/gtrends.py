import csv, datetime, time
import re, sys, logging
import httplib, urllib, urllib2

from pattern import web
from cookielib import CookieJar

GOOG_USER = 'skyinvestments99@gmail.com'
GOOG_PASS = 'gamingthesystem'

class pyGTrends(object):
    """
    Google Trends API
    
    Recommended usage:
    
    from csv import DictReader
    r = pyGTrends(username, password)
    r.download_report(('pants', 'skirt'))
    d = DictReader(r.csv().split('\n'))
    """
    def __init__(self, username, password):
        """
        provide login and password to be used to connect to Google Analytics
        all immutable system variables are also defined here
        website_id is the ID of the specific site on google analytics
        """        
        self.login_params = {
            "continue": 'http://www.google.com/trends',
            "PersistentCookie": "yes",
            "Email": username,
            "Passwd": password,
        }
        self.headers = [("Referrer", "https://www.google.com/accounts/ServiceLoginBoxAuth"),
                        ("Content-type", "application/x-www-form-urlencoded"),
                        ('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1042.0 Safari/535.21'),
                        ("Accept", "text/plain")]
        self.url_ServiceLoginBoxAuth = 'https://accounts.google.com/ServiceLoginBoxAuth'
        self.url_Export = 'http://www.google.com/trends/viz'
        self.url_CookieCheck = 'https://www.google.com/accounts/CheckCookie?chtml=LoginDoneHtml'
        self.url_PrefCookie = 'http://www.google.com'
        self.header_dictionary = {}
        self._connect()
        
    def _connect(self):
        """
        connect to Google Trends
        """
        self.cj = CookieJar()                            
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        self.opener.addheaders = self.headers
        
        resp = self.opener.open(self.url_ServiceLoginBoxAuth).read()
        resp = re.sub(r'\s\s+', ' ', resp)
        dom = web.Element(resp)
        self.login_params['GALX'] = dom.by_attr(name='GALX')[0].attributes['value']
        params = urllib.urlencode(self.login_params)
        self.opener.open(self.url_ServiceLoginBoxAuth, params)
        self.opener.open(self.url_CookieCheck)
        self.opener.open(self.url_PrefCookie)
        
    def download_report(self, keywords, date='2013-11', geo='all', geor='all', graph = 'all_csv', sort=0, scale=0, sa='N'):
        """
        download a specific report
        date, geo, geor, graph, sort, scale and sa
        are all Google Trends specific ways to slice the data
        """
        if type(keywords) not in (type([]), type(('tuple',))):
            keywords = [keywords]
        
        params = urllib.urlencode({
            'q': ",".join(keywords),
            'date': date,
            'graph': graph,
            'geo': geo,
            'geor': geor,
            'sort': str(sort),
            'scale': str(scale),
            'sa': sa
        })                            
        self.raw_data = self.opener.open('http://www.google.com/trends/viz?' + params).read()
        if self.raw_data in ['You must be signed in to export data from Google Trends']:
            logging.error('You must be signed in to export data from Google Trends')
            raise Exception(self.raw_data)
        
    def csv(self, section="Main", as_list=False):
        """
        Returns a CSV of a specific segment of the data.
        Available segments include Main, City and Subregion.
        """
        if section == "Main":
            section = ("Week","Year","Day","Month")
        else:
            section = (section,)
            
        segments = self.raw_data.split('\n\n\n')
    
        # problem in that we didnt skip the first 4 lines which usually contain information
        # such as Web Search interest: debt, United States; 2004 - present, Interest over time ...
        start = []
        found = False
        for i in range(len(segments)):
            lines = segments[i].split('\n')
            n = len(lines)
            for counter, line in enumerate(lines):
                if line.partition(',')[0] in section or found:
                    if counter + 1  != n: # stops us appending a stupid blank newspace at the end of the file
                        start.append(line + '\n')
                    else:
                        start.append(line)
                    found = True

            segments[i] = ''.join(start)    

        for s in segments:
            if s.partition(',')[0] in section:
                if as_list:
                    return [line for line in csv.reader(s.split('\n'))]
                else:
                    return s
            logging.error("Could not find requested section")            
            raise Exception("Could not find requested section")

    def getData( self):
        return self.raw_data

    def writer( self, outputname = "report.csv" ) :
        o = open(outputname, "wb")
        o.write( self.raw_data )

"""
getGoogleTrendData(search_query, filename, date, geo, scale, position)

Saves the Google Trend data for the given search_query as filename.

Arguments
=========
search_query (string):
    The search query for which to retrieve data.

filename (string):
    The filename to save the data file under.

date (string):
    A date in the format YYYY, YYYY-MM, YYYY-MM-DD. If you specify the year, you'll
    retrieve weekly trends over a year. If you specify a month, you'll retrieve daily
    trends over a month.

geo (string):
    The geographic section for which to retrieve trends.

scale (string):
    The scale at which to retrive the data.

position (string):
    Should not be modified until you want to specify the position of the csv being generated.

Returns
=======
This function does not return a value.
"""
def getGoogleTrendData(search_query, filename=None, date="2013-11", geo="all", scale="1", position="end"):
    # connect to the Google Trends website
    connector = pyGTrends(GOOG_USER, GOOG_PASS)
    connector.download_report(search_query, date=date, geo=geo, scale=scale)
    data = connector.csv(section='Main').split('\n')
    csv_reader = csv.reader(data)

    # remove all whitespaces
    search_query = search_query.strip() 
    search_query = " ".join(search_query.split())
    search_query = search_query.replace(" ", "")

    # if no filename is specified, choose our own
    if filename == None:
        filename = search_query + '_trend.csv'

    # write out the csv
    with open(filename, 'w') as csv_out:
        positionInWeek = { "start" : 0, "end" : 1 }
        separator = " - "
        csv_writer = csv.writer( csv_out )

        for count, row in enumerate( csv_reader ):
            if separator not in row[0] : 
                csv_writer.writerow( row )
                continue

            date = row[0].split(separator)[positionInWeek[position]] 

            # we want to remove any whitespaces from the value entry since we are not interested in blank data points
            val = re.sub(r'\s+', '', row[1] )
            if len(val) < 1 :
                continue

            if count == 0:
                csv_writer.writerow( row )
            else:
                csv_writer.writerow( [ str(date) ] + [ str(val) ])