# -*- coding: utf-8 -*-
"""
Created on Mon Jun 08 15:58:46 2015

@author: Epoch
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 09:28:42 2015

@author: bluecap

en esto file hacemos la conexion con un server de mysql y se tira las tablas 
"""

import MySQLdb
import string
import datetime 
import pandas as pd
from datetime import datetime

from bs4 import BeautifulSoup
import requests
import sys
import os
os.chdir("C:\\Users\\Epoch\\Documents\\GitHub\\scraper-project\\python")
import nltk.data
from nltk.tokenize import WordPunctTokenizer, wordpunct_tokenize
import pandas as pd
import nltk
import re, codecs
from __future__ import division
from nltk.stem.snowball import SnowballStemmer
import numpy as np
from datetime import datetime, timedelta
# a naive and incomplete demonstration on how to read a *.spydata file
import lda
import itertools
import time


     
host = "bluecap.cubz34n4knn2.eu-central-1.rds.amazonaws.com"
user = "bluecap"
password = "Bluecap2005"
dbname = "einformaDB"

db = MySQLdb.connect(host, user, password, dbname)
cursor = db.cursor()


##### Necessary functions ####

def tiraTextoBS(url) :
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    text1 = soup.find_all('p')
    text2 = [a.getText() for a in text1]
    textFinal = " ".join(text2)
    return textFinal

def relevanceMeter1(docTokens, dictionary):
    # conta cuanto vezes los terminos en diccionario apparecen en texto
    elemsIn = [elem for elem in dictionary if elem in docTokens]
    n = len(elemsIn)
    relevance = n/len(dictionary)

    return (relevance)  

def relevanceMeter2(docTokens, dictionary):
    # conta cuanto vezes los terminos en diccionario apparecen en texto - conta mas que un tiempo cada palabra si esta en el texto mas que un vez
    elemsIn = [docTokens.count(elem) for elem in dictionary]
    n = sum(elemsIn)
    relevance = n/len(dictionary)

    return (relevance)    
    
def compare_lists(x, y):
     count = 0
     for num in y:
             if num in x:
                     count += 1
     return count
    
def relevanceWeighted(docTokens, dictionaryDescr, empresaName, texto, weightFactor) :
        # conta cuanto vezes los terminos en diccionario apparecen en texto
    elemsIn = [elem for elem in dictionaryDescr if elem in docTokens]
    #elemsInAct = [elem for elem in empresaNameVec if elem in docTokens]
    n1 = len(elemsIn)
    n2 = 0
    #print empresaName
    #print empresaName
    if empresaName in texto :
        n2 = 1

    relevance = n1/len(dictionaryDescr) + n2*(weightFactor)
    return (relevance)
    
    
def construirVecFechas(nombres_fechas, df) :
    nombresVec = df["empresa"]
    vec_concurso = []
    for nom in nombresVec :
        temp = nombres_fechas[nombres_fechas["nom_limpios"].replace("'", "") == nom.replace("'", "")]
        #print temp['fecha_concurso'].values[0]
        vec_concurso.append(temp['fecha_concurso'].values[0])
    dfNew = df
    dfNew['fecha_de_concurso_de_empresa']= pd.DataFrame(vec_concurso)
    return(dfNew)
    

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



#### get first few rows
# query1 = "select*from einformaDB.eInforma_Empresas limit 5;"
# top5= cursor.execute(query1)

queryConcurso = "SELECT * FROM einformaDB.Empresas where situacion like '%Concurso%'and situacion like '%CONCURSO%' ;"

df = pd.read_sql(queryConcurso, db)
nombres = list(df['nombre_empresa'])


###################################
# cleaning names and getting dates for concurso
    
badTerms = ["SL", "SA", "S.L.", "SOCIEDAD", "ANONIMA", "LIMITADA", "SCCL"]
 
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


###################################
queryNoticias = "SELECT * FROM einformaDB.PeriodicosGrandes5 group by link;"
noticiasDF = pd.read_sql(queryNoticias, db) # has text missing for some reason...

### Updating some text
ind = 0
for link in noticiasDF["link"] :
    texto = tiraTextoBS(str(link))
    noticiasDF.iloc[ind, 7] = texto
    print "... finished updating text for %s noticia out of %s ..." % (ind, len(noticiasDF))
    ind+=1
    if ind % 100 == 0 :
        try : 
            noticiasDF.to_sql(con=db, name='noticias_concurso', if_exists='replace', flavor='mysql')
        except :
            db = MySQLdb.connect(host, user, password, dbname)
            cursor = db.cursor()
            noticiasDF.to_sql(con=db, name='noticias_concurso', if_exists='replace', flavor='mysql')
            print "...  error ... ", sys.exc_info()[0]

# updating some text 
           
new_noticias_df =construirVecFechas(nombres_fechas, noticiasDF)        

## Solo donde fecha_concurso > fecha_noticia
new_noticias_df["fecha"] = pd.to_datetime(new_noticias_df["fecha"])
new_noticias_df["fecha_de_concurso_de_empresa"] = pd.to_datetime(new_noticias_df["fecha_de_concurso_de_empresa"])   

nombresLimp = [unicode(a, "utf8").encode("utf8") for a in dfAll["nombre_empresa"]]
dfAll["nombresLimp"] = pd.DataFrame(nombresLimp)
  
textData = list(new_noticias_df['texto'])
textDataMerged = [unicode(a, "utf-8") for a in textData]


## Setting up 
dfConKeywords = pd.DataFrame()
ind = 0
for nom in new_noticias_df["empresa"] :
    for empr in dfAll :
        
        temp = dfAll[dfAll["nombre_empresa"].str.contains(nom)]
    #cleanNameDF = pd.DataFrame(nom) 
    
    tempDF = [dfConKeywords, temp[['nombre_provincia', 'CNAE1_name', 'objeto_social', 'nombre_empresa']]]
    dfConKeywords = pd.concat(tempDF)
    ind +=1
    
listEmpr = nombresLimpiador(list(dfConKeywords['nombre_empresa']), badTerms)
dfConKeywords = dfConKeywords.reset_index(drop=True)
dfConKeywords['nombre_empresa'] = pd.DataFrame(listEmpr)

dictConKeyWords = {}

for i in range(0, dfConKeywords.shape[0]) :
    listKeyWords = str(dfConKeywords.iloc[i, -1]).split()+str(dfConKeywords.iloc[i, -2]).split()+str(dfConKeywords.iloc[i, -3]).split()+str(dfConKeywords.iloc[i, -4]).split()
    
    dictConKeyWords[dfConKeywords.iloc[i, -1]] = " ".join(listKeyWords)


# removando stopwords
dictConKeyWords2 = {}
for empr in dictConKeyWords :
    tempDoc = RawDocsMod1(unicode(dictConKeyWords[empr], "utf8"), "stopWEsp.txt")
    tempDoc.token_clean()
    tempDoc.stopword_remove()
    tok = tempDoc.tokens
    dictConKeyWords2[empr] = tok    
    
    
new_noticias_df["relevance1"] = np.nan
new_noticias_df["relevance2"] = np.nan


relevanceList1 = []
relevanceList2 = []

#rel2 = relevanceWeighted(cleanTokens, descripcion, listo_de_nombre_de_empresa, 3)

for articulo in range(0, new_noticias_df.shape[0]) :
    text = unicode(new_noticias_df.iloc[articulo, 7], "utf8")
    rawDocs = RawDocsMod1(text, "stopWEsp.txt")
    rawDocs.token_clean()
    rawDocs.stopword_remove()
    cleanTokens = rawDocs.tokens
    nombreEmpresa = new_noticias_df.iloc[articulo, 1]
    try :
        descripcion = dictConKeyWords2[nombreEmpresa]
        rel1 = relevanceMeter1(cleanTokens, descripcion)
        rel2 = relevanceWeighted(cleanTokens, descripcion, unicode(nombreEmpresa, "utf8").lower(), unicode(new_noticias_df.iloc[articulo, 7], "utf8").lower(),3)
        
        relevanceList1.append(rel1)
        relevanceList2.append(rel2)
        new_noticias_df.iloc[articulo, 10] = rel1
        new_noticias_df.iloc[articulo, 11] = rel2
        print " ++++ encontro empresa %s " % nombreEmpresa
    except :
        print sys.exc_info()[0]
        print "--- no encontro empresa %s " % nombreEmpresa    # when there is an error matching empresas




    

