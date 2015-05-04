# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:04:25 2015

@author: bluecap

proxy = urllib2.ProxyHandler({'http': '127.0.0.1'})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)
"""
import os
os.chdir("C:\\Users\\bluecap\\Desktop\\bluecap\\soft\\pygoogle3")

import time
from bs4 import BeautifulSoup                    # For processing HTML
import urllib  
import json                             # URL tools
import re                                        # Regular expressions
import requests
from google import search
from pygoogle import pygoogle
from pygoogle3 import pygoogle3

prox = {'http': 'http://37.59.230.179:7808'}
filehandle = urllib.urlopen('http://google.com', proxies=prox)

g = pygoogle("ALDARAJE SL")
g.pages = 5
print '*Found %s results*'%(g.get_result_count())
urlList = g.get_urls()
titleList = g.search()

googleInfo2 = {}
googleInfo3 = {}
searchTerms = nombres # + actual more specific search terms
searchTermsCut = searchTerms[0:2]
name = searchTermsCut[0]
for name in searchTermsCut :
    #### ABSOLUTMENTE NECESITO A USIR UN METODO CON PROXY PARA BUSCAR A GOOGLE AQUI!!!!!
    # ind = searchTermsCut.index(name)
    g = pygoogle3(name)
    g.pages = 5
    googleInfo2[name] = list(g.get_urls())
    googleInfo3[name] = list(g.search())
    g = None
    print " going to sleep goodnight"
    time.sleep(5)

def showsome(searchfor):
  query = urllib.urlencode({'q': searchfor})
  url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
  
  
  #response = requests.get(url) 
  #time.sleep(rest)
  #soup = response.text
  search_response = urllib2.urlopen(url)
  search_results = search_response.read()
  results = json.loads(search_results)
  data = results['responseData']
  print 'Total results: %s' % data['cursor']['estimatedResultCount']
  hits = data['results']
  print 'Top %d hits:' % len(hits)
  for h in hits: print ' ', h['url']
  print 'For more results, see %s' % data['cursor']['moreResultsUrl']
  return results['responseData']
  
showsome("hello world")
####################################################
### NEW STUFF #####################################



































