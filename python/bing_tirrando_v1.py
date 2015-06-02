# -*- coding: utf-8 -*-
"""
Created on Tue May 12 09:56:57 2015

@author: bluecap
se usa Noticias.py para recolectar articulos mientras consiguiendo codigo en Noticias.py - tienes que correr los funciones por dentrolo anterior que corriendo estas aquí 
"""

__autor__ = "Yevgeniy Levin" 

import MySQLdb
import string
from bs4 import BeautifulSoup
import re
import time
import sys
import os
from selenium import webdriver
import pandas as pd

os.chdir("C:\\Users\\bluecap\\Desktop\\bluecap\\project\\scrapper\\python")
badTerms = ["SL", "SA", "S.L.", "SOCIEDAD", "ANONIMA", "LIMITADA", "SCCL"]

def nombresLimpiador(nombresVec, terms) :
    nombresNuevos = []
    punct = set(string.punctuation)
    if type(nombresVec) == list :
        for nom in nombresVec :
            nomList = nom.split()
            nomNew = [''.join(x for x in a if x not in punct) for a in nomList if a not in terms]
            nombresNuevos.append(" ".join(nomNew))  
            #print "shouldnt be this"
    else : 
        #print "should be this"
        nomList = nombresVec.split()
        nomNew = [''.join(x for x in a if x not in punct) for a in nomList if a not in terms]
        nombresNuevos = " ".join(nomNew)
        
    return(nombresNuevos)

#### Conectando a baso de datos y tirando empresas con concurso
host = "bluecap.cubz34n4knn2.eu-central-1.rds.amazonaws.com"
user = "bluecap"
password = "Bluecap2005"
dbname = "einformaDB"

#DROP TABLE IF EXISTS bingNoticias;
create_table = """ 
CREATE TABLE einformaDB.bingNoticiasTodo
(
empresa text,
fecha text,
autor text,
link text, 
parrafo text, 
titulo text
);"""

db = MySQLdb.connect(host, user, password, dbname)
cursor = db.cursor()

# creiando la tabla con bing cosas 
cursor.execute("DROP TABLE IF EXISTS einformaDB.bingNoticiasTodo;")
cursor.execute(create_table)

queryConcurso = "SELECT * FROM einformaDB.Empresas where situacion like '%Concurso%';"
nombres_fechas = pd.DataFrame()
dfAll = pd.read_sql(queryConcurso, db)
nombres_fechas[['nombre_empresa', 'situacion']] = dfAll[['nombre_empresa', 'situacion']]
nombresNuevos = nombresLimpiador(nombresLimpiador(list(nombres_fechas['nombre_empresa']), badTerms), badTerms)
nombres_fechas[['nom_limpios']] = pd.DataFrame(nombresNuevos)
fechasALimpiar = list(nombres_fechas['situacion'])
fechas = [a[a.index(":") + 1:a.rindex(")")] for a in fechasALimpiar]
fechas =[a[1:] for a in fechas]
nombres_fechas[['fecha_concurso']] = pd.DataFrame(fechas) 
nombres_fechas = nombres_fechas[['nom_limpios', 'fecha_concurso']]


''' Bing SEARCH '''
"BingNews(keys, wait=0)"
'''''''''''''''''''' 
driver = webdriver.Chrome()

# VERIFICA EL NOMBRE DE LA TABLA !!!!!!!!!!!!!!!!!!!!!!
insertString = "INSERT INTO einformaDB.bingNoticiasTodo (empresa, fecha, autor, link, parrafo, titulo)  values (%s, %s, %s, %s, %s, %s);"

    

###############################################################

""" El resto es para probar cosas variadas """
##############################################################
#### Tratando con mas vinculos que hay un primera pagina


def BingNews2(key, wait=0) :
    
    # go to the google home page
    driver.get("https://www.bing.com/?scope=news")
    # find the element that's name attribute is q (the google search box)
    inputElement = driver.find_element_by_id("sb_form_q")
    # type in the search
    inputElement.send_keys(key)
    # submit the form (although google automatically searches now without submitting)
    inputElement.submit()
    resultados = []
    
    nextPageBool = 0 # si queremos ir a la proxima pagina para repetir el mismo que en primera lo sera =1
    pageDoing = 1
    def gatherAll() :
        for res in driver.find_elements_by_class_name('sn_r'):
            noticia = {}
            titulo = res.find_element_by_tag_name('a').text
            link = res.find_element_by_tag_name('a').get_attribute('href')
            fecha = res.find_element_by_css_selector('.sn_tm').text
            fuente = res.find_element_by_css_selector('.sn_src').text
            parrafo = res.find_element_by_css_selector('.sn_snip').text
            noticia['Empresa']=key
            noticia['titulo']=titulo
            noticia['link']=link
            noticia['fecha']=fecha
            noticia['autor']=fuente
            noticia['parrafo']=parrafo
            resultados.append(noticia)
            
    
    try:
        
        #Nos movemos a lo largo de todos los resultados de la búsqueda extrayendo la info 
        gatherAll()
        while nextPageBool == 0 :
            try :
                temp = driver.find_element_by_class_name("sb_pagN")
                temp.click()
                gatherAll()
                pageDoing +=1 
                print "scraping pagina no. %s" % pageDoing
            except :
                print "no hay mas paginas con resultados"
                nextPageBool = 1
                
                
            print nextPageBool
            time.sleep(wait)
            
        return(resultados)
            
    except:
        print('Ha ocurrido un error con la busqueda de '+key)
        print("Unexpected error:", sys.exc_info())
        time.sleep(2)  
        
   
''' Bing SEARCH '''
"BingNews(keys, wait=0)"
'''''''''''''''''''' 
driver = webdriver.Chrome()

insertString = "INSERT INTO einformaDB.bingNoticias (empresa, fecha, autor, link, parrafo, titulo)  values (%s, %s, %s, %s, %s, %s);"

def updateDBBing(empresaDict, baseString) :
    # se hace updating MYSQL DB 
    for nom in empresaDict:
        if len(empresaDict[nom])>0 :
            for articulo in empresaDict[nom] :
                tempDF = pd.DataFrame(articulo.items())
                print "Se actualizo empresa '%s' y articulo se llama '%s' " % (unicode(nom, "utf-8").encode("utf-8"), tempDF.iloc[5, 1].encode("utf-8"))
                cursor.execute(baseString, (tempDF.iloc[0, 1].encode("utf-8"), tempDF.iloc[1, 1].encode("utf-8"), tempDF.iloc[2, 1].encode("utf-8"), tempDF.iloc[3, 1].encode("utf-8"), tempDF.iloc[4, 1].encode("utf-8"), tempDF.iloc[5, 1].encode("utf-8"))) 
                db.commit()


## attacando bing 
todasEmpresas = {}
paraActualisarDB = {} # un diccionario temporario
noms = list(nombres_fechas['nom_limpios'])
ind = 0
cadaN_updateDB = 10
N = len(noms)
for nom in noms :
    #if ind > 252 :
    infoList = BingNews2(key=nom.decode("utf-8"), wait=2)
    todasEmpresas[nom.decode("utf-8")] = infoList
    paraActualisarDB[nom.decode("utf-8")] = infoList
    print "he terminado yendo a yahoo para sacar info sobre empresa # %s de %s " % (ind, N)
    if ind >0 and ind%cadaN_updateDB==0 :
        updateDBBing(paraActualisarDB, insertString)
        paraActualisarDB = {}
    ind +=1