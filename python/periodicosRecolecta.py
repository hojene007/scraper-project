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
#os.system("taskkill /im chrome.exe")

import sys  


#reload(sys)  
#sys.setdefaultencoding('utf-8')


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

"""    
#############################################################################

#############################################################################  
    
############### Attacando periodicos españoles
""""""

#queryConcurso = "SELECT * FROM einformaDB.Empresas where situacion like '%Concurso%' and situacion like '%CONCURSO%';"
dropIfthere = "DROP TABLE IF EXISTS einformaDB.PeriodicosGrandes5;"
nuevaTabla = """CREATE TABLE einformaDB.PeriodicosGrandes5
(
fuenta text,
empresa text,
fecha text,
autor text,
link text, 
parrafo text, 
titulo text,
texto text
);"""
#cursor.execute(dropIfthere)
#cursor.execute(nuevaTabla)

insertString = "INSERT INTO einformaDB.PeriodicosGrandes5(fuenta, empresa, fecha, autor, link, parrafo, titulo, texto)  values (%s, %s, %s, %s, %s, %s, %s, %s);"

"""
def updateDBPeriodicosGrandes(fuenta, empresaDict, baseString) :
    # se hace updating MYSQL DB 
    for nom in empresaDict:
        if len(empresaDict[nom])>0 :
            for articulo in empresaDict[nom] :
                tempDF = pd.DataFrame(articulo.items())
                print "Se actualizo empresa '%s' y articulo se llama '%s' " % (nom.encode("utf-8"), tempDF.iloc[5, 1].encode("utf-8"))
                cursor.execute(baseString, (fuenta, tempDF.iloc[0, 1].encode("utf-8"), tempDF.iloc[1, 1].encode("utf-8"), tempDF.iloc[2, 1].encode("utf-8"), tempDF.iloc[3, 1].encode("utf-8"), tempDF.iloc[4, 1].encode("utf-8"), tempDF.iloc[5, 1].encode("utf-8"),  tempDF.iloc[6, 1].encode("utf-8"))) 
                db.commit()
"""
def updateDBPeriodicosGrandes2(fuenta, empresaDict, baseString) :
    for nom in empresaDict:
        if len(empresaDict) > 0:
            for articulo in empresaDict[nom] :    
                print "Actualizo empresa %s  y articulo con titulo %s " % (unicode(articulo["Empresa"], "utf-8").encode("utf-8"), articulo["titulo"].encode("utf-8"))
                cursor.execute(baseString, (fuenta, unicode(articulo["Empresa"], "utf-8").encode("utf-8"), articulo["fecha"].encode("utf-8"), articulo["autor"].encode("utf-8"), articulo["link"].encode("utf-8"), articulo["parrafo"].encode("utf-8"), articulo["titulo"].encode("utf-8"), articulo["texto"].encode("utf-8")))
                db.commit()


dictElPais = {}
dictElMundo = {}
dictExpansion = {}

paraActualisarExpansion = {}
paraActualisarElMundo = {}
paraActualisarElPais = {} # un diccionario temporario

noms = list(nombres_fechas['nom_limpios'])
ind = 115
cadaN_updateDB = 5
N = len(noms)
indexError = 0

try :
    for nom in noms :
        # para bigNoticias3 acabadó a 280
        if noms.index(nom) > -1 and noms.index(nom) < 1302:     
                ind= noms.index(nom)
                
                
                print "...........Yendo a Expansion............"
                
                
                try :
                    expansionTemp = ExpansionTP2("'"+nom+"'", wait=2)
                    if len(expansionTemp) > 0 :
                        for link in expansionTemp :
                            index = expansionTemp.index(link)
                            print ".... cogiendo noticia %s de %s .....Expansion" % (index, len(expansionTemp))
                            if index != 0 and index%30 == 0:
                                driver.quit()
                                #os.system("taskkill /im chrome.exe")
                                driver = webdriver.Chrome()
                            link["texto"] = tiraExpansion(link["link"])
                except :
                    driver = webdriver.Chrome()
                    expansionTemp = ExpansionTP2("'"+nom+"'", wait=2)
                    if len(expansionTemp) > 0 :
                        for link in expansionTemp :
                            index = expansionTemp.index(link)
                            print ".... cogiendo noticia %s de %s .....Expansion" % (index, len(expansionTemp))
                            if index != 0 and index%30 == 0:
                                driver.quit()
                                #os.system("taskkill /im chrome.exe")
                                driver = webdriver.Chrome()
                            link["texto"] = tiraExpansion(link["link"])
                            
                            
                    
                print "...........Yendo a El Mundo............"
                
                
                
                try :
                    elmundoTemp = ElMundoTP2("'"+nom+"'", wait=2)
                    if len(elmundoTemp)> 0 :
                        for link in elmundoTemp :
                            index = elmundoTemp.index(link)
                            print ".... cogiendo noticia %s de %s .....El Mundo" % (index, len(elmundoTemp))
                            if index != 0 and index%30 == 0:
                                driver.quit()
                               # os.system("taskkill /im chrome.exe")
                                driver = webdriver.Chrome()
                            link["texto"] = tiraElMundo(link["link"]) # seguiendo a cada vinculo
                except :
                    driver = webdriver.Chrome()
                    elmundoTemp = ElMundoTP2("'"+nom+"'", wait=2)
                    if len(elmundoTemp)> 0 :
                        for link in elmundoTemp :
                            index = elmundoTemp.index(link)
                            print ".... cogiendo noticia %s de %s .....El Mundo" % (index, len(elmundoTemp))
                            if index != 0 and index%30 == 0:
                                driver.quit()
                                #os.system("taskkill /im chrome.exe")
                                driver = webdriver.Chrome()
                            link["texto"] = tiraElMundo(link["link"]) # seguiendo a cada vinculo
                            
                            
                    
                print "...........Yendo a El Pais............"   
                
                
                try :
                    elpaisTemp = ElPaisTP2("'"+nom+"'", wait =2) # variables temopranias que contenen la busqueda en cada periodoco empresa se llama "nom"
                    if len(elpaisTemp) > 0 :
                        for link in elpaisTemp :
                            index = elpaisTemp.index(link)
                            print ".... cogiendo noticia %s de %s .....El Pais" % (index, len(elpaisTemp))
                            if index != 0 and index%30 == 0:
                                driver.quit()
                                os.system("taskkill /im chrome.exe") # limpiando los procesos para no se paran chrome 
                                driver = webdriver.Chrome()
                            link["texto"] = tiraElPais(link["link"]) 
                except :
                    driver = webdriver.Chrome()
                    elpaisTemp = ElPaisTP2("'"+nom+"'", wait =2) # variables temopranias que contenen la busqueda en cada periodoco empresa se llama "nom"
                    if len(elpaisTemp) > 0 :
                        for link in elpaisTemp :
                            index = elpaisTemp.index(link)
                            print ".... cogiendo noticia %s de %s .....El Pais" % (index, len(elpaisTemp))
                            if index != 0 and index%30 == 0:
                                driver.quit()
                                os.system("taskkill /im chrome.exe") # limpiando los procesos para no se paran chrome 
                                driver = webdriver.Chrome()
                            link["texto"] = tiraElPais(link["link"]) 
                            
                            
                
                dictExpansion[nom.decode("utf-8")] = expansionTemp
                dictElMundo[nom.decode("utf-8")] = elmundoTemp
                dictElPais[nom.decode("utf-8")] = elpaisTemp
                
                
                
                paraActualisarExpansion[nom.decode("utf-8")] = expansionTemp
                paraActualisarElMundo[nom.decode("utf-8")] = elmundoTemp
                paraActualisarElPais[nom.decode("utf-8")] = elpaisTemp
                
                
                
                print "he terminado yendo a yahoo para sacar info sobre empresa # %s de %s " % (ind, N)
                if ind >0 and ind%cadaN_updateDB==0 :
                    try :
                        updateDBPeriodicosGrandes2("expansion", paraActualisarExpansion, insertString)
                        updateDBPeriodicosGrandes2("elmundo", paraActualisarElMundo, insertString)
                        updateDBPeriodicosGrandes2("elpais", paraActualisarElPais, insertString)
                    except :
                        db = MySQLdb.connect(host, user, password, dbname)
                        cursor = db.cursor()
                        updateDBPeriodicosGrandes2("expansion", paraActualisarExpansion, insertString)
                        updateDBPeriodicosGrandes2("elmundo", paraActualisarElMundo, insertString)
                        updateDBPeriodicosGrandes2("elpais", paraActualisarElPais, insertString)
                        
                    paraActualisarExpansion = {}
                    paraActualisarElMundo = {}
                    paraActualisarElPais = {}
except WebDriverException :
      for nom in noms :
        # para bigNoticias3 acabadó a 280
        if noms.index(nom) > ind :     
                ind= noms.index(nom)
                
                
                print "...........Yendo a Expansion............"
                
                
                try :
                    expansionTemp = ExpansionTP2("'"+nom+"'", wait=2)
                    if len(expansionTemp) > 0 :
                        for link in expansionTemp :
                            index = expansionTemp.index(link)
                            print ".... cogiendo noticia %s de %s .....Expansion" % (index, len(expansionTemp))
                            if index != 0 and index%30 == 0:
                                driver.quit()
                                #os.system("taskkill /im chrome.exe")
                                driver = webdriver.Chrome()
                            link["texto"] = tiraExpansion(link["link"])
                except :
                    driver = webdriver.Chrome()
                    expansionTemp = ExpansionTP2("'"+nom+"'", wait=2)
                    if len(expansionTemp) > 0 :
                        for link in expansionTemp :
                            index = expansionTemp.index(link)
                            print ".... cogiendo noticia %s de %s .....Expansion" % (index, len(expansionTemp))
                            if index != 0 and index%30 == 0:
                                driver.quit()
                                #os.system("taskkill /im chrome.exe")
                                driver = webdriver.Chrome()
                            link["texto"] = tiraExpansion(link["link"])
                            
                            
                    
                print "...........Yendo a El Mundo............"
                
                
                
                try :
                    elmundoTemp = ElMundoTP2("'"+nom+"'", wait=2)
                    if len(elmundoTemp)> 0 :
                        for link in elmundoTemp :
                            index = elmundoTemp.index(link)
                            print ".... cogiendo noticia %s de %s .....El Mundo" % (index, len(elmundoTemp))
                            if index != 0 and index%30 == 0:
                                driver.quit()
                               # os.system("taskkill /im chrome.exe")
                                driver = webdriver.Chrome()
                            link["texto"] = tiraElMundo(link["link"]) # seguiendo a cada vinculo
                except :
                    driver = webdriver.Chrome()
                    elmundoTemp = ElMundoTP2("'"+nom+"'", wait=2)
                    if len(elmundoTemp)> 0 :
                        for link in elmundoTemp :
                            index = elmundoTemp.index(link)
                            print ".... cogiendo noticia %s de %s .....El Mundo" % (index, len(elmundoTemp))
                            if index != 0 and index%30 == 0:
                                driver.quit()
                                #os.system("taskkill /im chrome.exe")
                                driver = webdriver.Chrome()
                            link["texto"] = tiraElMundo(link["link"]) # seguiendo a cada vinculo
                            
                            
                    
                print "...........Yendo a El Pais............"   
                
                
                try :
                    elpaisTemp = ElPaisTP2("'"+nom+"'", wait =2) # variables temopranias que contenen la busqueda en cada periodoco empresa se llama "nom"
                    if len(elpaisTemp) > 0 :
                        for link in elpaisTemp :
                            index = elpaisTemp.index(link)
                            print ".... cogiendo noticia %s de %s .....El Pais" % (index, len(elpaisTemp))
                            if index != 0 and index%30 == 0:
                                driver.quit()
                                os.system("taskkill /im chrome.exe") # limpiando los procesos para no se paran chrome 
                                driver = webdriver.Chrome()
                            link["texto"] = tiraElPais(link["link"]) 
                except :
                    driver = webdriver.Chrome()
                    elpaisTemp = ElPaisTP2("'"+nom+"'", wait =2) # variables temopranias que contenen la busqueda en cada periodoco empresa se llama "nom"
                    if len(elpaisTemp) > 0 :
                        for link in elpaisTemp :
                            index = elpaisTemp.index(link)
                            print ".... cogiendo noticia %s de %s .....El Pais" % (index, len(elpaisTemp))
                            if index != 0 and index%30 == 0:
                                driver.quit()
                                os.system("taskkill /im chrome.exe") # limpiando los procesos para no se paran chrome 
                                driver = webdriver.Chrome()
                            link["texto"] = tiraElPais(link["link"]) 
                            
                            
                
                dictExpansion[nom.decode("utf-8")] = expansionTemp
                dictElMundo[nom.decode("utf-8")] = elmundoTemp
                dictElPais[nom.decode("utf-8")] = elpaisTemp
                
                
                
                paraActualisarExpansion[nom.decode("utf-8")] = expansionTemp
                paraActualisarElMundo[nom.decode("utf-8")] = elmundoTemp
                paraActualisarElPais[nom.decode("utf-8")] = elpaisTemp
                
                
                
                print "he terminado yendo a yahoo para sacar info sobre empresa # %s de %s " % (ind, N)
                if ind >0 and ind%cadaN_updateDB==0 :
                    try :
                        updateDBPeriodicosGrandes2("expansion", paraActualisarExpansion, insertString)
                        updateDBPeriodicosGrandes2("elmundo", paraActualisarElMundo, insertString)
                        updateDBPeriodicosGrandes2("elpais", paraActualisarElPais, insertString)
                    except :
                        db = MySQLdb.connect(host, user, password, dbname)
                        cursor = db.cursor()
                        updateDBPeriodicosGrandes2("expansion", paraActualisarExpansion, insertString)
                        updateDBPeriodicosGrandes2("elmundo", paraActualisarElMundo, insertString)
                        updateDBPeriodicosGrandes2("elpais", paraActualisarElPais, insertString)
                        
                    paraActualisarExpansion = {}
                    paraActualisarElMundo = {}
                    paraActualisarElPais = {}
    
except KeyboardInterrupt : 
    print "Master says stop!"




