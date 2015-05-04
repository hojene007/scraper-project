# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 12:36:16 2015

@author: bluecap
"""

## Manual google search
import requests
from bs4 import BeautifulSoup
import re
import time

urlRoot = "https://www.google.es/"
proxyList = ['http://5.107.161.14:8118', 'http://200.84.171.98:8080']


def queryConv(query) :
    # se converse un query a un que se puede estar leido para urlopen
    temp = query.split()
    result = '+'.join(temp)
    return '#q='+result
    
urlNew = urlRoot+queryConv('ALDARAJE SL')

response0 = requests.get(urlNew, proxies={'http': proxyList[0]})
soup0 = BeautifulSoup(response0.text)

pattern = re.compile(r'\data-href(.+?)\"', soup0.text)
