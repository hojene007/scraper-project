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

db = MySQLdb.connect(host, user, password, dbname)
cursor = db.cursor()

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


''' YAHOO SEARCH '''
"YahooNews(keys, wait=0)"
'''''''''''''''''''' 
todasEmpresas = {}

for nom in list(nombres_fechas[['nom_lipios']]) :
    infoList = YahooNews(key=nom, wait=2)
    todasEmpresas[nom] = infoList





