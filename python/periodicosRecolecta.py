# -*- coding: utf-8 -*-
"""
Created on Tue May 12 09:56:57 2015

@author: bluecap
se usa Noticias.py para recolectar articulos mientras consiguiendo codigo en Noticias.py - tienes que correr los funciones por dentrolo anterior que corriendo estas aquí 
"""

import MySQLdb
import string
from bs4 import BeautifulSoup
import re
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

### Conectando a baso de datos y tirando empresas con concurso
host = "bluecap.cubz34n4knn2.eu-central-1.rds.amazonaws.com"
user = "bluecap"
password = "Bluecap2005"
dbname = "einformaDB"#

db = MySQLdb.connect(host, user, password, dbname)
cursor = db.cursor()

# creiando la tabla con bing cosas 3
#cursor.execute("DROP TABLE IF EXISTS einformaDB.bingNoticias;")
#cursor.execute(create_table)

queryConcurso = "SELECT * FROM einformaDB.Empresas where situacion like '%Concurso%' and situacion like '%CONCURSO%';"
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

"""
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
                print "Se actualizo empresa '%s' y articulo se llama '%s' " % (nom.encode("utf-8"), tempDF.iloc[5, 1].encode("utf-8"))
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
    infoList = BingNews(key=nom.decode("utf-8"), wait=2)
    todasEmpresas[nom.decode("utf-8")] = infoList
    paraActualisarDB[nom.decode("utf-8")] = infoList
    print "he terminado yendo a yahoo para sacar info sobre empresa # %s de %s " % (ind, N)
    if ind >0 and ind%cadaN_updateDB==0 :
        updateDBBing(paraActualisarDB, insertString)
        paraActualisarDB = {}
    ind +=1
"""    
#############################################################################

#############################################################################  
    
############### Attacando periodicos españoles
queryConcurso = "SELECT * FROM einformaDB.Empresas where situacion like '%Concurso%' and situacion like '%CONCURSO%';"
dropIfthere = "DROP TABLE IF EXISTS einformaDB.PeriodicosGrandes;"
nuevaTabla = """CREATE TABLE einformaDB.PeriodicosGrandes
(
fuenta text,
empresa text,
fecha datetime,
autor text,
link text, 
parrafo text, 
titulo text,
texto text
);"""
cursor.execute(dropIfthere)
cursor.execute(nuevaTabla)
insertString = "INSERT INTO einformaDB.PeriodicosGrandes (fuenta, empresa, fecha, autor, link, parrafo, titulo, texto)  values (%s, %s, %s, %s, %s, %s, %s, %s);"


def updateDBPeriodicosGrandes(fuenta, empresaDict, baseString) :
    # se hace updating MYSQL DB 
    for nom in empresaDict:
        if len(empresaDict[nom])>0 :
            for articulo in empresaDict[nom] :
                tempDF = pd.DataFrame(articulo.items())
                print "Se actualizo empresa '%s' y articulo se llama '%s' " % (nom.encode("utf-8"), tempDF.iloc[5, 1].encode("utf-8"))
                cursor.execute(baseString, (fuenta, tempDF.iloc[0, 1].encode("utf-8"), tempDF.iloc[1, 1].encode("utf-8"), tempDF.iloc[2, 1].encode("utf-8"), tempDF.iloc[3, 1].encode("utf-8"), tempDF.iloc[4, 1].encode("utf-8"), tempDF.iloc[5, 1].encode("utf-8"),  tempDF.iloc[6, 1].encode("utf-8"))) 
                db.commit()

dictElPais = {}
dictElMundo = {}
dictExpansion = {}

paraActualisarExpansion = {}
paraActualisarElMundo = {}
paraActualisarElPais = {} # un diccionario temporario

noms = list(nombres_fechas['nom_limpios'])
ind = 0
cadaN_updateDB = 10
N = len(noms)
indexError = 0
for nom in noms :
    while indexError > -1 :
        indexError +=1
    
        expansionTemp = ExpansionTP2(nom, wait=2)
        print "...........Yendo a Expansion............"
        for link in expansionTemp :
            index = expansionTemp.index(link)
            print ".... cogiendo noticia %s de %s .....Expansion" % (index, len(expansionTemp))
            if index != 0 and index%100 == 0:
                driver.quit()
                driver = webdriver.Chrome()
            expansionTemp[index]["texto"] = tiraExpansion(expansionTemp[index]["link"])
            
            
            
        elmundoTemp = ElMundoTP2(nom, wait=2)
        print "...........Yendo a El Mundo............"
        for link in elmundoTemp :
            index = elmundoTemp.index(link)
            print ".... cogiendo noticia %s de %s .....El Mundo" % (index, len(elmundoTemp))
            if index != 0 and index%100 == 0:
                driver.quit()
                driver = webdriver.Chrome()
            elmundoTemp[index]["texto"] = tiraElMundo(elmundoTemp[index]["link"]) # seguiendo a cada vinculo
            
            
           
        elpaisTemp = ElPaisTP2(nom, wait =2) # variables temopranias que contenen la busqueda en cada periodoco empresa se llama "nom"
        print "...........Yendo a El Pais............"
        for link in elpaisTemp :
            index = elpaisTemp.index(link)
            print ".... cogiendo noticia %s de %s .....El Pais" % (index, len(elpaisTemp))
            if index != 0 and index%100 == 0:
                driver.quit()
                driver = webdriver.Chrome()
            elpaisTemp[index]["texto"] = tiraElPais(elpaisTemp[index]["link"]) 
        
        
        dictExpansion[nom.decode("utf-8")] = expansionTemp
        dictElMundo[nom.decode("utf-8")] = elmundoTemp
        dictElPais[nom.decode("utf-8")] = elmundoTemp
        
        paraActualisarExpansion[nom.decode("utf-8")] = expansionTemp
        paraActualisarElMundo[nom.decode("utf-8")] = elmundoTemp
        paraActualisarElPais[nom.decode("utf-8")] = elmundoTemp
        
        print "he terminado yendo a yahoo para sacar info sobre empresa # %s de %s " % (ind, N)
        if ind >0 and ind%cadaN_updateDB==0 :
            updateDBPeriodicosGrandes("expansion", paraActualisarExpansion, insertString)
            updateDBPeriodicosGrandes("elmundo", paraActualisarElMundo, insertString)
            updateDBPeriodicosGrandes("elpais", paraActualisarElPais, insertString)
            paraActualisarExpansion = {}
            paraActualisarElMundo = {}
            paraActualisarElPais = {}
        ind +=1


    
    
    
