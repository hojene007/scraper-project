# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 13:14:43 2015
http://www.crummy.com/software/BeautifulSoup/bs4/doc/
http://blog.miguelgrinberg.com/post/easy-web-scraping-with-python

Esto archivo hace scaping de http://www.einforma.com/ por crear un database de empresas espanoles


@author: Yevgeniy Levin
"""
############## Setup and helper functions
import requests
from bs4 import BeautifulSoup
import re
import time
import sys
   
def getEmpresaInfo(url) :
    # Esto function se necesita para seguir a pagina de la empresa y entonces tirar infos necesitos
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    table = soup.find(id="tablaInformesSuperetiqueta")
    errorVal = 'NoError'
    try :
        rawRowList = table.findAll('tr') 
    except :
        errorVal = "Houston we have a problem"
        rawRowList = list()
        
    rowDict = {}
    
    if errorVal == 'NoError' :
        for row in rawRowList :
            thisRow = row.findAll("td")
            k = len(thisRow)
            if k>1 :
                t1 = re.findall('.+', thisRow[0].text)
                t2 = re.findall('.+', thisRow[1].text)
                rowDict[str(t1)] = ([t2])
            elif k==1 :
                t1 = re.findall('.+', thisRow[0].text)
                rowDict["otraInfo"] = ([t1])
    else :
        rowDict["otraInfo"] = ["no info sobre empresa"]
        print("no info sobre empresa")
    
    return rowDict

####### Implementation for the first page 

url1 = 'http://www.einforma.com/empresas/CNAE.html'
response1 = requests.get(url1)
soup1 = BeautifulSoup(response1.text)
linksList1 = [a.attrs.get('href') for a in soup1.select('div.mod-content.last a[href^=http://www.einforma.com]')]
linksList1 = list(set(linksList1)) # getting unique elements
namesList = [a.contents for a in soup1.select('div.mod-content.last a[href^=http://www.einforma.com]')]
namesList1 = [x[0].encode("utf-8") for x in namesList]
namesList2 = [re.findall(r">(.*)\<", x) for x in namesList1]
namesList3 = filter(None, namesList2) # list of names of companies on page

empresaListo = {} # creando el primero vez el dictionary de empresas
for link in linksList1 :
    i = linksList1.index(link)
    empresaListo[namesList3[i][0]] = getEmpresaInfo(link)
    print("Empresa numero {}, se llama {}".format(i+1, namesList3[i][0]), time.strftime("%H:%M:%S"))
    
    
## yendo a la proxima pagina
urlRoot = "http://www.einforma.com"
url2 =  "http://www.einforma.com/empresas/CNAE/Empresa-2.html"
response2 = requests.get(url2)
soup2 = BeautifulSoup(response2.text)
backForward = [a.attrs.get('href') for a in soup2.select('div.col02 a[href^=/empresas]')]

### Perpetuating loop until the end of pages
while len(backForward)>2 :
    newUrl = urlRoot+backForward[1]
    responseNew = requests.get(newUrl)
    soupNew = BeautifulSoup(responseNew.text)
    ## Name of company list creation
    namesListNew = [a.contents for a in soupNew.select('div.mod-content.last                 a[href^=http://www.einforma.com]')]
    namesListNew1 = [x[0].encode("utf-8") for x in namesListNew]
    namesListNew2 = [re.findall(r">(.*)\<", x) for x in namesListNew1]
    namesListNew3 = filter(None, namesListNew2) # list of names of companies on page
    
    ## List of links creation
    linksListNew1 = [a.attrs.get('href') for a in soupNew.select('div.mod-content.last a[href^=http://www.einforma.com]')]
    linksListNew1 = list(set(linksListNew1)) # getting unique elements
    
    ### extracting data
    for link in linksListNew1 :
        i = linksListNew1.index(link)
        empresaListo[namesListNew3[i][0]] = getEmpresaInfo(link)
        print("Empresa numero {}, se llama {}".format(len(empresaListo)+1, namesListNew3[i][0]), time.strftime("%H:%M:%S"))
        print(len(empresaListo))
    ### Updating variables for next round
    backForward = [a.attrs.get('href') for a in soupNew.select('div.col02 a[href^=/empresas]')]
    print(backForward[1])
    ### Cleaning variables used
    del namesListNew, namesListNew1, namesListNew2, namesListNew3, linksListNew1
