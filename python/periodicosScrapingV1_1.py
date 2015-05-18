# -*- coding: utf-8 -*-
"""
Created on Thu May 07 11:28:35 2015

@author: bluecap

esto script se leendo el baso de los datos de sql y tirando los nombres de las empresas - ahora solo para empresas con concurso
funcciona con 20minutos
"""

import requests
import MySQLdb
from bs4 import BeautifulSoup
import re
import re
import time
import sys
import os
import urllib2
import pygoogle
from mechanize import Browser
import nltk
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

os.chdir("C:\\Users\\bluecap\\Desktop\\bluecap\\project\\scrapper\\python")
url="http://www.20minutos.es/busqueda"
nltk.download() # <--------- run this!!
spanish_tokenizer = nltk.data.load("tokenizers/punkt/spanish.pickle") # <--------- run this!!


def q2Url(urlBase, quer):
    urlNew = urlBase+"?q="+quer
    return urlNew

def nombresLimpiador(nombresVec, terms) :
    nombresNuevos = []
    for nom in nombresVec :
        nomList = nltk.word_tokenize(nom)
        nomNew = filter(lambda a: a != terms, nomList)
        nombresNuevos.append(" ".join(nomNew))    
    return(nombresNuevos)
    
#### Conectando a baso de datos y tirando empresas con concurso
host = "bluecap.cubz34n4knn2.eu-central-1.rds.amazonaws.com"
user = "bluecap"
password = "Bluecap2005"
dbname = "einformaDB"

db = MySQLdb.connect(host, user, password, dbname)
cursor = db.cursor()

queryConcurso = "SELECT * FROM einformaDB.Empresas where situacion like '%Concurso%';"

dfAll = pd.read_sql(queryConcurso, db)
nombres = list(dfAll['nombre_empresa'])
nombresNew = nombresLimpiador(nombres, ["SL", "SA", "S.L.", "SOCIEDAD", "ANONIMA", "LIMITADA", "SCCL"])

empresasDict = {}
### El loop para todos de los empresas
nomLoop = 0
N = len(nombres)
for nom in nombres :
    
    # Create a new instance of the Firefox driver
    driver = webdriver.Chrome()

    # go to the google home page
    driver.get(q2Url(url, nom))
    # find the element that's name attribute is q (the google search box)
    #inputElement = driver.find_element_by_name("q")
    
    # type in the search
   # inputElement.send_keys(nom)
    
    # submit the form (although google automatically searches now without submitting)
    #inputElement.submit()
    
    baseText = driver.find_elements_by_css_selector('.gsc-tabdActive') #esto linea necesita hacer dos vezes - no se         porque todavia
    while len(baseText) == 0 :
        print "....Comprobando si base text se funcciona...."
        baseText = driver.find_elements_by_css_selector('.gsc-tabdActive')
    
    temp = baseText[0].text
    print temp
    
    ### Vinculos
# igualar los titulos de vinculos con los titulos de fechas
    links = driver.find_elements_by_css_selector('.gs-title')
    if len(links) > 0 :
        links1 = [link.get_attribute('href') for link in links if link.get_attribute('href') is not None]
        link2 = list(set(links1))
        linksAndTitulos = {}
        for link in links:
            #if str(link.get_attribute('href')) is not None :
            #   print(str(link.text.encode("utf-8"))+": "+str(link.get_attribute('href')))
            #print str(link.get_attribute('href'))
            
            if len(str(link.text.encode("utf-8")))>2:
                print(str(link.text.encode("utf-8")))
                linksAndTitulos[link.text.encode("utf-8")] = link.get_attribute('href')
                ##### limpiando los fechas
                fechas = re.findall('(?<=\n)(.*)(?=\s...)', temp)
                fechas = [a for a in fechas if a[0].isdigit()]
                fechas = [a.split()[0:3] for a in fechas]
                fechas = [" ".join(a) for a in fechas]
                fechas =[a for a in fechas if len(a)==11]
    
        ## Buscando titulos de texto completo
        titulosFecha =  re.findall('(?=www).*', temp)
        splitText = temp.split("www")
        newD = {}
        kkeys = linksAndTitulos.keys()
        kkeys = [a.decode("utf-8") for a in kkeys]
        for i in splitText:
            ind = splitText.index(i)
            for key in kkeys :
                if key in i:
                    tempL = list()
                    tempL.append(linksAndTitulos[key.encode("utf-8")])
                    tempL.append(fechas[ind])
                    newD[key.encode("utf-8")] = tempL
                    
        kkeys2 = newD.keys()
        ind = np.arange(len(fechas))
        cols = ['fuente', 'titulo', 'fecha', 'url', 'texto']
        df = pd.DataFrame(index=ind, columns = cols)
        
        loopN = 0
        for key in kkeys2 :
            responseNew = requests.get(newD[key][0].encode("utf-8"))
            soupNew = BeautifulSoup(responseNew.text)
            myText = soupNew.select('div.article-content')
            if len(myText) > 0 :
                textRaw = myText[0].encode("utf-8") # necesito a limpiarlo mas para tener solo el texto
            else : 
                textRaw =  "no hay text en esto vinculo"
            row = ['20minutos', linksAndTitulos[key.encode("utf-8")], newD[key][1].encode("utf-8"), newD[key][0].encode("utf-8"), textRaw]
            df.loc[loopN] = row
            #print("Result no %s " % loopN)
            loopN +=1
            del row
    else :
        df= "no hay articulos sobre esta empresa en fuente 20 minutos"
    nomLoop += 1
    empresasDict[nom] = df
    driver.quit()
    del df
    print ("Finished with info on %s ...... numero de empresas se acabado = %s de %s " % (nom, nomLoop, N))



