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
os.chdir("C:\\Users\\bluecap\\Documents\\GitHub\\scraper-project\\python")
from raw_docs import RawDocs3
import nltk.data
from nltk.tokenize import WordPunctTokenizer, wordpunct_tokenize
import pandas as pd
import nltk
import re, codecs
from __future__ import division
from sklearn import lda
from nltk.stem.snowball import SnowballStemmer
from gensim import corpora, models, similarities
import lda
import codecs
import lda.datasets
import enchant
import matplotlib.pyplot as plt
#print(SnowballStemmer("spanish").stem(unicode("maravilló", "utf8"))


#nltk.download()
os.chdir("C:\\Users\\bluecap\\Documents\\GitHub\\scraper-project\\documents")

spanish_dict = codecs.open('es.dic', encoding='utf-8')

#os.chdir("C:\\Users\\bluecap\\Desktop\\bluecap")
stopW1 = open("stopWEsp.txt")
spanish_tokenizer = nltk.data.load('tokenizers/punkt/spanish.pickle')

nombresLimp = [unicode(a, "utf8").encode("utf8") for a in dfAll["nombre_empresa"]]
dfAll["nombresLimp"] = pd.DataFrame(nombresLimp)
##########################################################################

""" Medidas de relevancia"""

##########################################################################
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
    
def relevanceWeighted(docTokens, dictionaryDescr, dictionaryActivity, weightFactor) :
        # conta cuanto vezes los terminos en diccionario apparecen en texto
    elemsIn = [elem for elem in dictionaryDescr if elem in docTokens]
    elemsInAct = [elem for elem in dictionaryActivity if elem in docTokens]
    n1 = len(elemsIn)
    n2 = len(elemsInAct)
    relevance = n1/len(dictionaryDescr) + n2*weightFactor/len(elemsInAct)
    return (relevance)

###########################################################################

""" Analisís para articulos relevantes """

###########################################################################
"""
#####################################################################
### estoy creando un listo para cada negocio que vas a decirme el rating de cada articulo 
#####################################################################
necesario a correr sqlPull.py
"""

"""
#trunctDF = [dfAll[dfAll["nombresLimp"].str.contains(articulos_relevantes2["empresa"][a].str)] for a in articulos_relevantes2["empresa"]]
nombres = [art.split() for art in articulos_relevantes2['empresa']]

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
    
"""

##############################################################################

""" And now for all the noticias available - testing relevanceMeter"""     
#################################################################
## 

#new_noticias_df["relevance"] = np.nan

textData = list(new_noticias_df['texto'])
textDataMerged = [unicode(a, "utf-8") for a in textData]

## Setting up 
dfConKeywords = pd.DataFrame()
ind = 0
for nom in new_noticias_df["empresa"] :
    for empr in dfAll :
        
        temp = dfAll[dfAll["nombresLimp"].str.contains(nom)]
    #cleanNameDF = pd.DataFrame(nom) 
    
    tempDF = [dfConKeywords, temp[['nombre_provincia', 'CNAE1_name', 'objeto_social', 'nombresLimp']]]
    dfConKeywords = pd.concat(tempDF)
    ind +=1
    
#listEmpr = nombresLimpiador(list(dfConKeywords['nombresLimp']), badTerms)
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
        rel1 = relevanceMeter1(cleanTokens, descripcion)
        print "hola!"
        rel2 = relevanceMeter2(cleanTokens, descripcion)
        
        relevanceList1.append(rel1)
        relevanceList2.append(rel2)
        new_noticias_df.iloc[articulo, 10] = rel1
        new_noticias_df.iloc[articulo, 11] = rel2
        print " ++++ encontro empresa %s " % nombreEmpresa
    except :
        print "--- no encontro empresa %s " % nombreEmpresa 


####### Plots of relevance
n_bins = 10
rel1 = new_noticias_df[["relevance1"]].sort(["relevance1"], ascending = 0)
rel2 = new_noticias_df[["relevance2"]].sort(["relevance2"], ascending = 0)
index = range(0, toPlot.shape[0])
plt.plot(index, rel1, 'r--', label = "p\_1")
plt.plot(index, rel2, 'g--', label="p\_2")
plt.title('Relevance measure indicators')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)   # subplot 211 title


### Ve new_noticias_df para relevancia    

     
#######################################################################
""" LDA ANALISÍS """
#######################################################################

#### a primero vamos a limpiar text datos
allCorpus = []
allCorpStems = []

def getCleanToks(text_start) :
    text = text_start
    if type(text) !=  unicode :
        text = unicode(text_start, "utf8")
    
    rawDocs = RawDocsMod1(text, "stopWEsp.txt")
    rawDocs.token_clean()
    rawDocs.stopword_remove()
    rawDocs.stem()
    cleanTokens = rawDocs.tokens
    stems = rawDocs.stems
    return cleanTokens, stems

ind = 0
for articulo in range(0, new_noticias_df.shape[0]) :
    tokenStems = getCleanToks(new_noticias_df.iloc[articulo, 7])
    allCorpus +=tokenStems[0]
    allCorpStems += tokenStems[1]
    print ind
    ind +=1
        
palabrasUnicasCorpus = list(set(allCorpus))
stemsUnicosCorpus = list(set(allCorpStems))

pwl = enchant.request_pwl_dict("es.dic")
pwl.check("hola")

########### a crear un DTM   #####################


documentTermMat = pd.DataFrame()


docName = "doc %s"

index = 0
listOfLists = []
for articulo in range(0, new_noticias_df.shape[0]) :
    if index > -1 :
        listOfTerms = []
        cleanTokens = getCleanToks(new_noticias_df.iloc[articulo, 7])
        for term in palabrasUnicasCorpus :
            listOfTerms.append(cleanTokens.count(term))
            
        newName = docName % index
        listOfLists.append(listOfTerms)
        print newName
    index +=1

docTermReal = np.array(listOfLists)
        
model = lda.LDA(n_topics=10, n_iter=1500, random_state=1)
X = lda.datasets.load_reuters()


######################################################################


######################################################################

stemmer = SnowballStemmer("spanish")
aa =a.split()
stem = [stemmer.stem(b) for b in aa]


