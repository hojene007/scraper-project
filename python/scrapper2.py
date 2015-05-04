# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 19:08:21 2015
chernovik for building scrapper 
Uses info from
http://www.crummy.com/software/BeautifulSoup/bs4/doc/
http://blog.miguelgrinberg.com/post/easy-web-scraping-with-python

@author: Epoch
"""

import requests
from bs4 import BeautifulSoup
import pickle
import re
import datetime
import time
import pdb
from urlparse import urlparse
#import nlpk natural language processing toolkit here
import numpy as np
from unidecode import unidecode
import string
import unicodedata



t = urlparse(linksList1[0])
     
url = "http://www.einforma.com/servlet/app/prod/DATOS_DE/EMPRESA/EXPAL-SYSTEMS-SA-C_QTAxMDAxNDEx_de-MADRID.html"
url1 = 'http://www.einforma.com/empresas/CNAE.html'
########### Testing how dictionaries suit scraping the company page
response = requests.get(url)
soup = BeautifulSoup(response.text)
table = soup.find(id="tablaInformesSuperetiqueta")
rawRowList = table.findAll('tr') 
rowDict = {}

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
##########################################################

############ Now to create a loop that goes through each page and visits all the links for each company
response1 = requests.get(url1)
soup1 = BeautifulSoup(response1.text)
linksList1 = [a.attrs.get('href') for a in soup1.select('div.mod-content.last a[href^=http://www.einforma.com]')]
linksList1 = list(set(linksList1)) # getting unique elements
pathLinks = list()
for link in linksList1 :
    tempPath = urlparse(link)
    pathLinks.append(tempPath.path) # path podria contener el nombre de la empresa
    
namesList = [a.contents for a in soup1.select('div.mod-content.last a[href^=http://www.einforma.com]')]
namesList1 = [x[0].encode("utf-8") for x in namesList]
namesList2 = [re.findall(r">(.*)\<", x) for x in namesList1]
namesList3 = filter(None, namesList2)
namesList3_1 = [noPunct(name[0]) for name in namesList3] # list of names of companies on page

    
    
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
                rowDict[str(t1[0].encode("utf-8"))] = t2[0]
            elif k==1 :
                t1 = re.findall('.+', thisRow[0].text)
                rowDict["otraInfo"] = t1[0]
    else :
        rowDict["otraInfo"] = ["no info sobre empresa"]
        print("no info sobre empresa")
    
    return rowDict
    
def matchUrl(path, empresa) :
    # esta function es necesita para encontrar el pagina de la empresa correcta 
    # path es el sendero que se tenga el nombre de la empresa
    # el umrbral se signfica de majoritad de palabras que es necesita para classificar el link
    umbral = 0.8
    splitE = empresa.split()
    boolVec = list()
    for palabra in splitE :
        if spainFix(palabra) in path :
            boolVec.append(1)
        else :
            boolVec.append(0)
    if (sum(boolVec)/len(splitE))>=umbral :
        correct = 1
    else :
        correct = 0        
    return correct

def spainFix(myString) :
    # esto function se hace los caracteres español en el mas cerca carácters ingles
    bigN = 0
    smallN = 0
    newString = list(unidecode(myString))
    if "Ñ" in myString :
        bigN = 1
        indN = myString.index("Ñ")
        newString[indN] = "N"
    if "ñ" in myString :
        smallN = 1
        indNn = myString.index("ñ")
        newString[indNn] = "n"
    if "Ç" in myString :
        indC = myString.index("Ç")
        newString[indC] = "C"
    if "ç" in myString :
        indc = myString.index("ç")
        newString[indc] = "c"
        
    return "".join(newString)
    
def noPunct(myString) :
    # esta function se suprime el punctuacion de las frases 
    exclude = set(string.punctuation)
    s = ''.join(ch for ch in myString if ch not in exclude)
    return s

def keyChange1(myDict, newKeys) :
    # esta function se pone nueve nombre en uun key de dicconario 
    index = 0
    for i in myDict :
        myDict[newKeys] = newKeys[index]
        index =+ 1
     newDict = myDict
     return newDict
    
def keyChange2 (myDict, ref) :
    # esta function se cambia el keys del diccionario al los de ref (un diccianario por dentro myDict)
    # myRef = ref['Denominación']
    newDict = {}
    for cell in myDict :
        print cell
        name = myDict[cell][ref]
        newDict[name] = myDict[cell]        
    return newDict
    
urlTrueVec = list()
pp = linksList1[14]
for i in namesList3 :
    name = i[0]
    urlTrueVec.append(matchUrl(pp, name))
  
##########  
  
#########
  
########  

    
matchUrlVec = np.vectorize(matchUrl) # vectorised version
empresaListo = {}
for link in linksList1 :
    i = linksList1.index(link)
    urlTrueVec = list()
    for j in namesList3_1 :
        name = j
        urlTrueVec.append(matchUrl(pathLinks[i], name))
    empresaNombre = namesList3_1[urlTrueVec.index(1)]    
    empresaListo[empresaNombre] = getEmpresaInfo(link)
    print("Empresa numero {}, se llama {}".format(i+1, namesList3_1[urlTrueVec.index(1)]), time.strftime("%H:%M:%S"))
    
################# How to check if siguiente is present
urlRoot = "http://www.einforma.com"
url2 =  "http://www.einforma.com/empresas/CNAE/Empresa-2.html"
response2 = requests.get(url2)
soup2 = BeautifulSoup(response2.text)
backForward = [a.attrs.get('href') for a in soup2.select('div.col02 a[href^=/empresas]')]

# el condicion de parar el loop sera basado en el tamano de backForward ----- if len(backForward) < 4 break else keep scaping
backForward[1] =  "/empresas/CNAE/Empresa-100.html"

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
    
    ### Updating variables for next round
    backForward = [a.attrs.get('href') for a in soupNew.select('div.col02 a[href^=/empresas]')]
    
        
    ### Cleaning variables used
    del namesListNew, namesListNew1, namesListNew2, namesListNew3, linksListNew1
    
    
 
urlTest =  'http://www.einforma.com/servlet/app/prod/DATOS_DE/EMPRESA/ECONOCOM-SPAIN-SA-C_QTc4ODM2OTk2_de-BARCELONA.html'
for liink in linksListNew1 :
    print liink
    temp = getEmpresaInfo(liink)
    
urlT = linksListNew1[3]    
temp = getEmpresaInfo(urlTest)
    

    
    
###########################################
### TESTING SOME NEW FUNCTIONS
    
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
                    rowDict[str(t1[0].encode("utf-8"))] = t2[0]
                elif k==1 :
                    t1 = re.findall('.+', thisRow[0].text)
                    rowDict["otraInfo"] = t1[0]
        else :
            rowDict["otraInfo"] = ["no info sobre empresa"]
            print("no info sobre empresa")
            
        datosComLink = 
        
        return rowDict

url = "http://www.einforma.com/servlet/app/prod/DATOS_DE/EMPRESA/EXPAL-SYSTEMS-SA-C_QTAxMDAxNDEx_de-MADRID.html"
response = requests.get(url)
soup = BeautifulSoup(response.text)   
datosComLink = soup.select('div.posrel.mt20 a[href^=/ventas]').get('href')
datosComLink[0].attrs.get('href')

############## Unas operaciones de jugando con nombres de diccionarios 

keysVec = empresaDict2['ACERIA DE ALAVA SA'].keys()
keysVec2 = [a.decode('ascii','ignore') for a in keysVec]
keysVec2 = [a.encode('utf-8') for a in keysVec2]
keysVec3 = [re.sub('[^A-Za-z0-9]+', '', a) for a in keysVec2]

def remove_accents(data):
    return ''.join(x for x in unicodedata.normalize('NFKD', data) if x in string.ascii_letters).lower()
    
remove_accents(a.decode())

    
    
    
    
    
    



