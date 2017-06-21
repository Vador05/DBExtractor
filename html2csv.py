#!/usr/bin/env python3


import sys
import urllib
from argparse import ArgumentParser
from bs4 import BeautifulSoup
#import xlwt # will be used in future to export directly to excel.



def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument('-u', '--url', help='url to grab from')
    parser.add_argument('-n', '--num', help='number of pages to grab', 
                        type=int, default=10)
    parser.add_argument('-t', '--table', help='number of table on the page'
                        ,type=int,default=1)
    args = parser.parse_args()
    print(args)
    return args


def parse_rows(rows):
    results = []
    for row in rows:
        table_headers = row.find_all('th')
        #if table_headers:
            #results.append([headers.get_text() for headers in table_headers])

        table_data = row.find_all('td')
        if table_data:
            results.append([data.get_text() for data in table_data])
	    #for data in table_data:
            # First Example
             #  results.append(data.get_text())
	     #  results.append('@') 
    return results


def main():

	#Default Values
        count = 1 #Nothing to do, just a index for the loop
        table = 1 #Index of the table on the page
        num = 10 #Number of pages to search
	    
            # Parse arguments
        args = parse_arguments()
        if args.url:
            url = args.url
        if args.num:
            num = args.num
        if args.table:
            table = args.table

        while (count <= num):
            url = url + str(count)
            count = count+1
	    # Get the webpage
            try:
                resp = urllib.request.urlopen(url)
            except urllib.error.URLError as e:
                print ('An error occured fetching %s \n %s' % (url, e.reason))
                return 1
            soup = BeautifulSoup(resp.read())
	
	    # Find the table
            try:
                table = soup.find_all('table')[table]
            except AttributeError as e:
                print ('No tables found, exiting')
                return 1
	
	    # Read all rows
            try:
                rows = table.find_all('tr')
            except AttributeError as e:
                print ('No table rows found, exiting')
                return 1
	
            table_data = parse_rows(rows)
	    # Print data
            for i in table_data:
                print (';'.join(i))
	    #print(table_data)
	
if __name__ == '__main__':
    status = main()
    sys.exit(status)
