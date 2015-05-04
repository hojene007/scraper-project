# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 10:52:43 2015

File involves initial attempt at scrapping using python scrapping guide found on 
http://docs.python-guide.org/en/latest/scenarios/scrape/
http://blog.miguelgrinberg.com/post/easy-web-scraping-with-python
@author: bluecap
"""

from lxml import html
import requests
import bs4
import re 

urlRoot = 'http://www.einforma.com/empresas/CNAE.html'
page = requests.get(urlRoot)
tree = html.fromstring(page.text)
soup = bs4.BeautifulSoup(page.text)
linkNames = [a.attrs.get('href') for a in soup.select('div.mod-content.last a[href^=http://www.einforma.com]')]
linksList = [a.attrs.get('href') for a in soup.select('div.mod-content a[href^=/empresas]')]
namesList = [a.contents for a in soup.select('div.mod-content a[href^=/empresas]')]
temp = re.findall(r"'(.*?)'", str(namesList), re.DOTALL)

def scanLinks () :
    # function scans the root_url html for href links based on theme and returns a dictionary of 
    # links and names of their names ----- theme contains 4 elements - tag, tag name, subtag (unique element),
    # tag name
    # used in - webscrapping at Bluecap
    linksList = [a.attrs.get('href') for a in soup.select('div.mod-content last a[href^=http://www.einforma.com]')]


####
industryList = tree.xpath('//td[@title="first"]/text()')
