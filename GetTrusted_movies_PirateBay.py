# get the good trusted movie links form piratebay

############################################################
#import the external modules needed
import sys          #basic systm stuff
#import nltk        #NLTK (Natural Language Toolkit)
import urllib       #basic http stuff
#import urllib2      #new http stuff
#import webkit      #advanced http stuff, browser simulation for dynamic content
#import mechanize    #advanced http stuff, browser simulation for dynamic content
import commands
#import datetime
import os           #files, etc.
#import csv         #working with csv files
#import time
#import random
#import linecache
#import webbrowser
#import BeautifulSoup  #html parser & tools
import re           #regex, reserved chars are: . ^ $ * + ? { [ ] \ | ( )

#global variables
#example url 'http://thepiratebay.se/browse/201/0/7' # page # is /0/
global urlp1
global urlp2
global urlp3
urlp1 = 'http://thepiratebay.se/browse/201/'
#urlp2 = '0' #page number (navigation)
urlp3 = '/7'
global content
content = '' #initialize content variable, used per page

############################################################
# functions denoted by def name(arguments):

def get_urls(pages):
    matches = []
    startpage = 0
    endpage = pages
    for page in range(startpage,endpage):
        page_url = urlp1 + str(page) + urlp3
        #print page_url
        cmd = 'phantomjs getpage_w_cookie.js ' + '\'' + page_url + '\''
        output = commands.getoutput(cmd)
        #match = re.search(r'<td>\n<div class=\"detName\">.+">(.+)</a>\n</div>\n<a href=\"(.+)" title="Download this torrent using magnet">.+<a href="/user/.+title="(.+)" style="',output) #title
        temp_matches = re.findall(r'<td>\n<div class=\"detName\">.+">(.+)</a>\n</div>\n<a href=\"(.+)" title="Download this torrent using magnet">.+<a href="/user/.+title="(.+)" style="',output) #title
        #matches becomes an arrays of tuples containing information about each item, e.g., Title, link, usertype
        matches.extend(temp_matches)
    return matches

def filter_good(string1):
    goods = ['brr','bdr','dvd']
    result = 0
    badresult = -1 * len(goods)
    for good in goods:
        #print string1.find(good)
        result = result + string1.find(good)
    if (result == badresult):
        return False
    else: return True

############################################################
#main program block
def main():
    args = sys.argv[1:] #set args to be set of arguments 1 to last
    if len(args) < 1:
        print "\n Needs 2 arguments:\n   1) page_depth \n"
        sys.exit(1)

    depth = sys.argv[1]
    fulllist = get_urls(int(depth))
    badlist = []
    #print list
    for item in fulllist:
        #print item
        #print item[0].lower() #regex group 1 is Title
        isgood = filter_good(item[0].lower())
        if isgood:
            #print 'good'
            foo = ''
        else:
            #print 'bad'
            badlist.append(fulllist.index(item))
    for idx in (sorted(badlist,reverse=True)):
        fulllist.pop(idx)
    for item in fulllist:
        print item[0]
        print item[1]
        print item[2]
        print '\n'
    utorurl = 'http://localhost:8080/gui/?action=add-url&s=magnet:?xt=urn:btih:dd2d51f51bbef4884e1b4e95661e30724f7743b7&amp;dn=A.Thousand.Words.2012.DVDRip.XviD-NeDiVx&amp;tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&amp;tr=udp%3A%2F%2Ftracker.publicbt.com%3A80&amp;tr=udp%3A%2F%2Ftracker.istole.it%3A6969&amp;tr=udp%3A%2F%2Ftracker.ccc.de%3A80'
    cmd = 'phantomjs getpage.js ' + '\'' + utorurl + '\''
    output = commands.getoutput(cmd)
    print output
    
    
if __name__ == '__main__':
  main()