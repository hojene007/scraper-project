# -*- coding: utf-8 -*-
"""
Created on Mon May 25 09:31:54 2015

@author: Epoch
"""

"""
Analysis de datos con nltk
corre sqlPull.py y raw_docs.py antes esto usando de archivo
"""
import os
os.chdir("C:\\Users\\Epoch\\Documents\\GitHub\\scraper-project\\python")
from raw_docs import RawDocs3
import nltk.data
from nltk.tokenize import WordPunctTokenizer, wordpunct_tokenize
import pandas as pd
import nltk
import re, codecs
from __future__ import division
from sklearn import lda
from nltk.stem.snowball import SnowballStemmer

#print(SnowballStemmer("spanish").stem(unicode("maravilló", "utf8"))


#nltk.download()
os.chdir("C:\\Users\\bluecap\\Documents\\GitHub\\scraper-project\\documents")

stopW1 = open("stopWEsp.txt")
spanish_tokenizer = nltk.data.load('tokenizers/punkt/spanish.pickle')



"""
for i in textData :
    tok = wordpunct_tokenize(unicode(i, "utf8"))

tokNew = []
for j in tok :
    noPunct = (re.sub(ur'[\W_]+', u'', j, flags=re.UNICODE))
    noNumbers = (re.sub(ur'[0-9_]+', u'', noPunct, flags=re.UNICODE))
    tokNew.append(noNumbers)
tokNew = set(tokNew) # no hay nada mas palabras ahora

""" 
"""
#####################################################################
### estoy creando un listo para cada negocio que vas a decirme el rating de cada articulo 
#####################################################################
necesario a correr sqlPull.py
"""

nombres = [art.split() for art in articulos_relevantes2['empresa']]
nombresLimp = [unicode(a, "utf8").encode("utf8") for a in dfAll["nombre_empresa"]]
dfAll["nombresLimp"] = pd.DataFrame(nombresLimp)
#trunctDF = [dfAll[dfAll["nombresLimp"].str.contains(articulos_relevantes2["empresa"][a].str)] for a in articulos_relevantes2["empresa"]]

dfConKeywords = pd.DataFrame()
ind = 0
for nom in articulos_relevantes2["empresa"] :
    temp = dfAll[dfAll["nombresLimp"].str.contains(nom)]
    #cleanNameDF = pd.DataFrame(nom) 
    
    tempDF = [dfConKeywords, temp[['nombre_provincia', 'CNAE1_name', 'objeto_social', 'nombresLimp']]]
    dfConKeywords = pd.concat(tempDF)
    ind +=1
    
listEmpr = nombresLimpiador(list(dfConKeywords['nombresLimp']), badTerms)
dfConKeywords = dfConKeywords.reset_index(drop=True)
dfConKeywords['nombresLimp'] = pd.DataFrame(listEmpr)

dictConKeyWords = {}

for i in range(0, dfConKeywords.shape[0]) :
    listKeyWords = str(dfConKeywords.iloc[i, -1]).split()+str(dfConKeywords.iloc[i, -2]).split()+str(dfConKeywords.iloc[i, -3]).split()+str(dfConKeywords.iloc[i, -4]).split()
    
    dictConKeyWords[dfConKeywords.iloc[i, -1]] = " ".join(listKeyWords)



textData = list(articulos_relevantes2['texto'])
textDataMerged = [unicode(a, "utf-8") for a in textData]

# removando stopwords
dictConKeyWords2 = {}
for empr in dictConKeyWords :
    tempDoc = RawDocsMod1(unicode(dictConKeyWords[empr], "utf8"), "stopWEsp.txt")
    tempDoc.token_clean()
    tempDoc.stopword_remove()
    tok = tempDoc.tokens
    dictConKeyWords2[empr] = tok


def relevanceMeter1(docTokens, dictionary):
    # conta cuanto vezes los terminos en diccionario apparecen en texto
    elemsIn = [elem for elem in dictionary if elem in docTokens]
    n = len(elemsIn)
    if n> 0:
        relevance = n/len(dictionary)
    else :
        relevance = 0
    return (relevance)  

def relevanceMeter2(docTokens, dictionary):
    # conta cuanto vezes los terminos en diccionario apparecen en texto - conta mas que un tiempo cada palabra si esta en el texto mas que un vez
    elemsIn = [docTokens.count(elem) for elem in dictionary]
    n = sum(elemsIn)
    if n> 0:
        relevance = n/len(dictionary)

    else :
        relevance = 0

    return (relevance)    


a = ["a", "b", "c"]
b = ["b", "b", "d"]

relevanceMeter2(a, b)

articulos_relevantes2["relevance"] = np.nan
relevanceList = []
for articulo in range(0, articulos_relevantes2.shape[0]) :
    text = unicode(articulos_relevantes2.iloc[articulo, 7], "utf8")
    rawDocs = RawDocsMod1(text, "stopWEsp.txt")
    rawDocs.token_clean()
    rawDocs.stopword_remove()
    cleanTokens = rawDocs.tokens
    nombreEmpresa = articulos_relevantes2.iloc[articulo, 1]
    try :
        rel = relevanceMeter1(cleanTokens, descripcion)
        descripcion = dictConKeyWords2[nombreEmpresa]
        relevanceList.append(rel)
        articulos_relevantes2.iloc[articulo, 11] = rel
        print " ++++ encontro empresa %s " % nombreEmpresa
    except :
        print "--- no encontro empresa %s " % nombreEmpresa 


thresholdRelevance = 0.2
articulos_relevantes3 = articulos_relevantes2[articulos_relevantes2["relevance"]>thresholdRelevance]
    
#################################################################
## And now for all the noticias available - testing relevanceMeter

new_noticias_df["relevance"] = np.nan

textData = list(new_noticias_df['texto'])
textDataMerged = [unicode(a, "utf-8") for a in textData]

## Setting up 
dfConKeywords = pd.DataFrame()
ind = 0
for nom in new_noticias_df["empresa"] :
    temp = dfAll[dfAll["nombresLimp"].str.contains(nom)]
    #cleanNameDF = pd.DataFrame(nom) 
    
    tempDF = [dfConKeywords, temp[['nombre_provincia', 'CNAE1_name', 'objeto_social', 'nombresLimp']]]
    dfConKeywords = pd.concat(tempDF)
    ind +=1
    
listEmpr = nombresLimpiador(list(dfConKeywords['nombresLimp']), badTerms)
dfConKeywords = dfConKeywords.reset_index(drop=True)
dfConKeywords['nombresLimp'] = pd.DataFrame(listEmpr)

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

for articulo in range(0, new_noticias_df.shape[0]) :
    text = unicode(new_noticias_df.iloc[articulo, 7], "utf8")
    rawDocs = RawDocsMod1(text, "stopWEsp.txt")
    rawDocs.token_clean()
    rawDocs.stopword_remove()
    cleanTokens = rawDocs.tokens
    nombreEmpresa = new_noticias_df.iloc[articulo, 1]
    try :
        descripcion = dictConKeyWords2[nombreEmpresa]
        #print descripcion
        rel1 = relevanceMeter1(cleanTokens, descripcion)
        rel2 = relevanceMeter2(cleanTokens, descripcion)
        relevanceList1.append(rel1)
        relevanceList2.append(rel2)
        new_noticias_df.iloc[articulo, 10] = rel1
        new_noticias_df.iloc[articulo, 11] = rel2
        print " ++++ encontro empresa %s " % nombreEmpresa
    except :
        print "--- no encontro empresa %s " % nombreEmpresa 
        
#######################################################################
        """ LDA ANALISÍS """
#######################################################################
        
