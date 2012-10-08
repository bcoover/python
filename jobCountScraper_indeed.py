# scrape job counts posted for a list of companies (from csv)
import sys
import commands
import urllib
import re
import datetime
import os
import csv
import time
import random

def getCompanyJobCount(company,days):
    urlp1 = 'http://www.indeed.com/jobs?as_cmp='
    urlp2 = '&jt=all&sr=directhire&fromage='
    urlp3 = '&psf=advsrch'
    url = urlp1  + company + urlp2 + days + urlp3
    #print url
    ufile = urllib.urlopen(url)
    for line in ufile:
        match = re.search(r'(Jobs \d+ to \d+ )of (\d+)',line) #find the job count string
        if match:
            count = match.group(2)
            return count

def main():
    args = sys.argv[1:]
    if not args:
        print '\n #script scrapes indeed.com for current jobcounts for companies \n  usage: script.py infile outfile \n    infile: csv with single column of companies names \n    outfile: any csv filename \n'
        sys.exit(1)
    infile = open(sys.argv[1],'r')
    outfile = sys.argv[2] #e.g., 'jobcounts.csv'
    qdays = '3'
    rundate = datetime.datetime.now().date()
    if os.path.exists(outfile):
        f = open(outfile,'a')
    else:
        headings = ('Company',',','JobCount',',','searchDate',',','searchDaysBack','\n')
        f = open(outfile,'w')
        f.writelines(headings)
            
    readcsv = csv.reader(infile) #e.g., companies.csv
    for row in readcsv:
        qcompany = urllib.quote(str(row[0]))
        rcount = getCompanyJobCount(qcompany,qdays)
        tuple = (urllib.unquote(qcompany),',',rcount,',',str(rundate),',',('-' + qdays),'\n')
        
        for item in tuple:
            f.write(str(item))    
        timer = random.randint(2,8) #randomize delay between requests to avoid bot detection
        print timer
        time.sleep(timer)
        print 'done sleeping'
    f.close()

if __name__ == '__main__':
  main()
