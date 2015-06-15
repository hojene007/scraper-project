# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 18:56:00 2015

@author: Enric Gilabert & Yevgeny Levin
"""

###########################################################################################
# LIBRERÍAS                                                                           #####
###########################################################################################

from nltk.tokenize import WordPunctTokenizer
from bs4 import BeautifulSoup
import requests
from nltk.stem import SnowballStemmer
from nltk.corpus import cess_esp as cess
from nltk import UnigramTagger as ut
from nltk import BigramTagger as bt
from nltk.corpus import stopwords
import re, string
from pymongo import MongoClient
import pandas as pd
import time
from datetime import datetime, date
import pylab as p
import numpy as np


'''
# Read the corpus into a list, 
# each entry in the list is one sentence.
cess_sents = cess.tagged_sents()

# Train the unigram tagger
uni_tag = ut(cess_sents)

sentence = "Hola , esta foo bar ."

# Tagger reads a list of tokens.
uni_tag.tag(sentence.split(" "))

# Split corpus into training and testing set.
train = int(len(cess_sents)*90/100) # 90%

# Train a bigram tagger with only training data.
bi_tag = bt(cess_sents[:train])

# Evaluates on testing data remaining 10%
bi_tag.evaluate(cess_sents[train+1:])

# Using the tagger.
bi_tag.tag(sentence.split(" "))
'''
###########################################################################################
# VARIABLES E IMPORTACION DE DICCIONARIOS                                             #####
###########################################################################################

badTerms = ["SL", "SA", "S.L.", "SOCIEDAD", "ANONIMA", "LIMITADA", "SCCL", "LIMITADA.", "S.A.", "S.C.C.L.", "SOCIETAT", "S.A", "S A", "SCP", "SLP", "SLL"]
stemmer = SnowballStemmer("spanish")
tokenizer = WordPunctTokenizer()
spanish_stops = set(stopwords.words('spanish'))

f = open('C:/Users/Bluecap/Documents/Python Scripts/eInforma/positive-words-es.txt', 'r')
positive = []
[positive.append(line.strip()) for line in f]
f.close()

f = open('C:/Users/Bluecap/Documents/Python Scripts/eInforma/negative-words-es.txt', 'r')
negative = []
[negative.append(line.strip()) for line in f]
f.close()

f = open('C:/Users/Bluecap/Documents/Python Scripts/eInforma/diccionario_empresas.txt', 'r')
dic_empresas = []
[dic_empresas.append(line.strip().lower()) for line in f]
f.close()

f = open('C:/Users/Bluecap/Documents/Python Scripts/eInforma/dic_empresas_generated.txt', 'r')
dic_empresas_gen = []
[dic_empresas_gen.append(line.strip().lower()) for line in f]
f.close()

headers = {'Accept-Encoding': 'identity, deflate, compress, gzip',
           'Accept': '*/*','User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}

cookie= {'uid':'W9g/8VVfHfplwTL2AzAyAg==#69209aef53130fdb6de5ffb6bc3822c0', '__gads':'ID=1802bd5d11c3cfde:T=1432296967:S=ALNI_MYTjRdO3G4NczeWmr8J-iAoKvs4XA', 'avisopc':'1', 's_vnum':'1435701600011%26vn%3D2', 's_fid':'26FFD3718CCAA0EA-0CE730C7D881C034', 's_nr':'1433757370231-Repeat', 's_invisit':'true', 's_lv':'1433757370233', 's_lv_s':'Less%20than%201%20day', 's_sq':'%5B%5BB%5D%5D', 's_cc':'true', 'crtTags':'ctol300%3B'}


###########################################################################################
# DEFINICION DE FUNCIONES UTILIZADAS                                                  #####
###########################################################################################

def getEmpresas(lista):
    companies = [noticia['Empresa'] for noticia in lista]
    return( [len(set(companies)) , list(set(companies))])
    
def makeSoup(url):
    try:
        source_code = requests.get(url, headers=headers)
        print(source_code.encoding)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)
        return(soup)
    except:
        print('No he podido hacer el soup de '+url)
        return("")
        
def relevanceMeter1(docTokens, dictionary):
    # conta cuanto vezes los terminos en diccionario apparecen en texto
    elemsIn = [] 
    elemsIn_count = []
    for elem in dictionary:
        if elem in docTokens:
            elemsIn.append(elem)
            elemsIn_count.append(docTokens.count(elem))
    
    n = len(elemsIn)
    n2 = sum(elemsIn_count)
    relevance = n/len(dictionary)
    relevance2 = n2/len(dictionary)
    return ([relevance,relevance2])  

def relevanceMeter2(docTokens, dictionary):
    # conta cuanto vezes los terminos en diccionario apparecen en texto - conta mas que un tiempo cada palabra si esta en el texto mas que un vez
    elemsIn = [docTokens.count(elem) for elem in dictionary]
    n = sum(elemsIn)
    relevance = n/len(dictionary)
    return(relevance)
       
def sentimenteMeter1(docTokens, dictionary):
    # conta cuanto vezes los terminos en diccionario apparecen en texto
    elemsIn = [elem for elem in dictionary if elem in docTokens]
    n = len(elemsIn)
    relevance = n/len(dictionary)
    return(relevance)  

def sentimentMeter2(docTokens, dictionary):
    # conta cuanto vezes los terminos en diccionario apparecen en texto - conta mas que un tiempo cada palabra si esta en el texto mas que un vez
    elemsIn = [docTokens.count(elem) for elem in dictionary]
    n = sum(elemsIn)
    relevance = n/len(dictionary)
    return(relevance)  
    
def remove_punctuation(text):
    return re.sub('[%s]' % re.escape(string.punctuation), ' ', text)
    
def replace_punctuation(text, replace):
    return re.sub('[%s]' % re.escape(string.punctuation), replace, text)
    
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
    
def processor(text):
    texto = text.lower()
    texto = remove_punctuation(texto)
    tokenized = tokenizer.tokenize(texto)
    tokenized_no_stop = [word for word in tokenized if word not in spanish_stops]
    stemmed = [stemmer.stem(word) for word in tokenized_no_stop]
    return(stemmed)
    
def spainFix(myString) :
    # esto function se hace los caracteres español en el mas cerca carácters ingles - necesito lower case
    newString = list(myString)
    
    if "ñ" in myString :
        indNn = myString.index("ñ")
        newString[indNn] = "n"
    if "ç" in myString :
        indc = myString.index("ç")
        newString[indc] = "c"
    if "é" in myString :
        indc = myString.index("é")
        newString[indc] = "e"
    if "í" in myString :
        indc = myString.index("í")
        newString[indc] = "i"
    if "ó" in myString :
        indc = myString.index("ó")
        newString[indc] = "o"
    if "ó" in myString :
        indc = myString.index("ó")
        newString[indc] = "o"
    if "á" in myString :
        indc = myString.index("á")
        newString[indc] = "a"
    if "ú" in myString :
        indc = myString.index("ú")
        newString[indc] = "u"
    return "".join(newString)
    
def generateDict(lista, rec):
    dictionary = []
    nest=1
    while (nest<=rec):
        rec_dictionary = []
        for word in lista:
            url = "http://lenguaje.com/cgi-bin/Thesauro.exe?edition_field="+spainFix(word.lower())+"&B1=Buscar"
            print(url)
            try:
                resultados = makeSoup(url)
                get = resultados.find('ul', {'class':'Synonyms'})
                for sinonim in get.findAll('li'):
                    my_list = [x.strip() for x in sinonim.text.split(",")]
                    rec_dictionary.extend(my_list)
            except Exception as e:
                print(e)
                continue
        lista = rec_dictionary
        rec_dictionary = [x for x in rec_dictionary if x not in dictionary]
        dictionary.extend(rec_dictionary)
        nest+=1
            
    return(dictionary)

#dictionario = generateDict(['bueno'],1)

###########################################################################################
# UNIFICAR TODAS LAS NOTICIAS EN UNA LISTA CON TODOS LOS DATOS DE LA EMPRESA ASOCIADA #####
###########################################################################################

print('####  UNIFICAR ####################')
#We connect to the databases
client = MongoClient()
db = client.social_hats
cursor = db.noticias.find({"texto":{"$ne":None}})
db2 = client.empresas_morosas

'''
count_ini = getEmpresas(list(cursor))
print(len(list(cursor)))
print(count_ini[0])
'''

noticias_relevantes = []
#We get all the companies
for k in cursor:
    num = db.noticias.find({"Empresa": k['Empresa']}).count()
    if num < 20:
        print(num)
        noticias_relevantes.append(k)


noticias = noticias_relevantes
concurso = list(db.concurso.find())
activas = list(db.activas.find())
morosos = list(db2.antoni.find())
N = len(noticias)

news_all = []

for i,noticia in enumerate(noticias):
    '''
    concurso_con_noticia = [x for x in concurso if noticia['Empresa'] in x['denominacion']]
    activas_con_noticia = [x for x in concurso if noticia['Empresa'] in x['denominacion']]
    morosos_con_noticia = [x for x in concurso if noticia['Empresa'] in x['Denominación:']]
    '''
    empresa = noticia['Empresa']
    print('- '+empresa+' '+str(i)+' / '+str(N)+' ('+"{0:.0f}%".format(float(i)/N* 100)+') --------------')
    concurso_con_noticia = list(db.concurso.find({"denominacion": {"$regex": u"^("+empresa+")."}}))
    if concurso_con_noticia:
        new = dict(concurso_con_noticia[0], **noticia)
        new['status'] = 'concurso'
        news_all.append(new)
        #db.news_all.insert_one(new)

    activas_con_noticia = list(db.activas.find({"denominacion": {"$regex": u"^("+empresa+")."}}))
    if activas_con_noticia:
        new = dict(activas_con_noticia[0], **noticia)
        new['status'] = 'activa'        
        news_all.append(new)
        #db.news_all.insert_one(new)
        
    morosos_con_noticia = list(db2.antoni.find({"Denominación:": {"$regex": u"^("+empresa+")."}}))
    if morosos_con_noticia:
        new = dict(morosos_con_noticia[0], **noticia)
        new['status'] = 'moroso' 
        news_all.append(new)
    
    if not concurso_con_noticia and not activas_con_noticia and not morosos_con_noticia:
        try:        
            print(empresa+' - '+new['denominacion'])
        except:
            print(empresa+' - '+new['Denominación:'])
        #db.news_all.insert_one(new)


print(len(concurso_con_noticia)) 
print(len(activas_con_noticia)) 
print(len(morosos_con_noticia))
print(len(news_all))



db.news_all_relevant.drop()
for new in news_all:
    new.pop("_id")
    
db.news_all_relevant.insert(news_all)
news_all_relevant = list(db.news_all_relevant.find())
###########################################################################################
# FILTRAR A TRAVES DE LA FECHA DE LA NOTICIA Y SITUACION                              #####
###########################################################################################
print('####  FILTRAR POR FECHA ####################')
new_filtered=[]
N = len(news_all)
db.new_filtered.drop()
now = datetime.now()
for i,new in enumerate(news_all):
    print('- '+str(i)+' / '+str(N)+' ('+"{0:.0f}%".format(float(i)/N* 100)+') --------------')
    if new['status'] is 'concurso':
        fecha_situacion = datetime.strptime(new['fecha_situacion'], "%d/%m/%Y")
        fecha_noticia = datetime.strptime(new['fecha'], "%d/%m/%Y")
        if fecha_situacion>fecha_noticia and datetime(fecha_situacion.year - 1,fecha_situacion.month,fecha_situacion.day)<fecha_noticia:
            new_filtered.append(new)
    else:
        if datetime.strptime(new['fecha'], "%d/%m/%Y") > datetime(now.year - 1,now.month,now.day):# now.timedelta(days=-365):#   
            new_filtered.append(new)

'''
db.new_filtered.drop()
for new in new_filtered:
    new.pop("_id")
'''
print(len(new_filtered))
getEmpresas((new_filtered))[0]

concurso = [x for x in new_filtered if x['status'] is 'concurso']
getEmpresas((concurso))
print(len(concurso))
print(count_ini[0])
db.new_filtered.insert(new_filtered)

count_ini = getEmpresas((new_filtered))

concurso = [x for x in new_filtered if x['status'] is 'concurso']
getEmpresas((concurso))
print(len((concurso)))
print(count_ini[0])

#new_filtered2 = list(db.new_filtered.find())
concurso = list(db.new_filtered.find({"status": 'concurso'}))
moroso = list(db.new_filtered.find({"status": 'moroso'}))
activa = list(db.new_filtered.find({"status": 'activa'}))
###########################################################################################
# FILTRAR POR RELEVANCIA                                                              #####
###########################################################################################

#for new in new_filtered:
    #    new.pop("_id")

def relevanceClassifier(x, thres):
    relevant = []
    N = len(x)    
    for i,new in enumerate(x):
        try:

            print('- Empresa '+new['status']+' - '+str(i)+' / '+str(N)+' ('+"{0:.0f}%".format(float(i)/N* 100)+') -- indexando relevancia...')
            # Crear tokens limpios del cuerpo de la noticia
            tokenized_text = processor(new['texto'])
            ind_empresa = relevanceMeter1(tokenized_text, dic_empresas)
            new['relevance1'] = ind_empresa[0]
            new['relevance2'] = ind_empresa[1]
            descriptions = ""
            for k,v in new.items():
                descriptions = " ".join((descriptions, str(v)))
            
            tokenized_description = processor(descriptions.lower())
            
            ind_description = relevanceMeter1(tokenized_text, tokenized_description)
            new['relevance3'] = ind_description[0]
            new['relevance4'] = ind_description[1]
            
            try:
                new['rel_ind'] = (new['relevance1']+thres*new['relevance3'])/(1+thres)
            except:
                new['rel_ind'] = 0
            
            relevant.append(new)
                
        except Exception as e:
            
            print(e)
            continue
        
    return(relevant)

#len(concurso)
#len(activa)
#new_filtered[50]
'''
sample = []
sample.extend(concurso)
sample.extend(activa)


relevant_news_concurso = relevanceClassifier(concurso, 2)
relevant_news_activa = relevanceClassifier(activa, 2)
'''

relevant_news = relevanceClassifier(new_filtered, 2)

rel_ind_list = []
for k in relevant_news:
    rel_ind_list.append(k['rel_ind'])

perc = np.percentile(rel_ind_list, 0)

relevant_news_filtered = [x for x in relevant_news if x['rel_ind']>perc]

'''
concurso = [x for x in relevant_news_filtered if x['status'] is 'concurso']
count = getEmpresas((concurso))
print(len(concurso))
print(count[0])

getEmpresas(relevant_news_filtered)
print(len(relevant_news_filtered))
'''
#p.hist(relevant_news)
###########################################################################################
# GENERACION DE SENTIMENT                                                             #####
###########################################################################################

#dic_empresas_gen = generateDict(dic_empresas,2)
#neg_dict = generateDict(['malo'],3)

#aux = set(neg_dict)
#neg_dict2 = list(aux)
'''
f = open('C:/Users/Bluecap/Documents/Python Scripts/eInforma/neg_dic_gen.txt', 'w')
for item in neg_dict:
  f.write("%s\n" % item)
f.close()

pos_dict = generateDict(['bueno'],3)

aux = set(pos_dict)
pos_dict2 = list(aux)

f = open('C:/Users/Bluecap/Documents/Python Scripts/eInforma/pos_dic_gen.txt', 'w')
for item in pos_dict:
  f.write("%s\n" % item)
f.close()
'''

f = open('C:/Users/Bluecap/Documents/Python Scripts/eInforma/pos_dic_gen.txt', 'r')
pos_dict2 = []
[pos_dict2.append(line.strip().lower()) for line in f]
f.close()

f = open('C:/Users/Bluecap/Documents/Python Scripts/eInforma/neg_dic_gen.txt', 'r')
neg_dict2 = []
[neg_dict2.append(line.strip().lower()) for line in f]
f.close()

pos_dict2 = list(set(pos_dict2))
neg_dict2 = list(set(neg_dict2))


def sentimentClassifier(list_of_news, k1, k2):
    
    k1 = k1
    k2 = k2
    
    tokens = []
    positive_stem = [stemmer.stem(word) for word in positive]
    negative_stem = [stemmer.stem(word) for word in negative]
    positive_stem2 = [stemmer.stem(word) for word in pos_dict2]
    negative_stem2 = [stemmer.stem(word) for word in neg_dict2]
    
    cursor = list_of_news
    
    classified = {}
    N = len(cursor)
    pos = 0
    pos2 = 0
    neg = 0
    neg2 = 0
    positive_count = 0
    negative_count = 0
    positive_count2 = 0
    negative_count2 = 0
    for i,new in enumerate(cursor):
        print('- Empresa '+str(i)+' / '+str(N)+' ('+"{0:.0f}%".format(float(i)/N* 100)+') --------------')
        texto = new['texto']
        texto = remove_punctuation(texto)
        tokenized = tokenizer.tokenize(texto)
        tokenized_no_stop = [word for word in tokenized if word not in spanish_stops]
        stemmed = [stemmer.stem(word) for word in tokenized_no_stop]
        
        
        pos = sentimenteMeter1(stemmed, positive_stem)
        pos2 = sentimenteMeter1(stemmed, positive_stem2)
        neg = sentimenteMeter1(stemmed, negative_stem)        
        neg2 = sentimenteMeter1(stemmed, negative_stem2)
        #posi = sentimentMeter2(stemmed, positive_stem)
        #negi = sentimentMeter2(stemmed, negative_stem)
        
        posIND = pos
        negIND = neg
        
        classified = new
        print(str(posIND)+' - '+str(negIND))
        if posIND>k1*negIND:
            positive_count += 1
            classified['sentiment'] = 'Postiva'
            print('1. Positiva - '+str(posIND)+' - '+str(negIND))
        elif posIND<k1*negIND:
            negative_count += 1
            classified['sentiment'] = 'Negativa'
            print('1. Negativa - '+str(posIND)+' - '+str(negIND))
        else:
            classified['sentiment'] = 'Neutra'
            print('1. Neutra - '+str(posIND)+' - '+str(negIND))
        
        
        posIND2 = pos2
        negIND2 = neg2
        
        if posIND2>k2*negIND2:
            positive_count2 += 1         
            classified['sentiment2'] = 'Postiva'
            print('2. Positiva - '+str(posIND2)+' - '+str(negIND2))
        elif posIND2<k2*negIND2:
            negative_count2 += 1
            classified['sentiment2'] = 'Negativa'
            print('2. Negativa - '+str(posIND2)+' - '+str(negIND2))
        else:
            classified['sentiment2'] = 'Neutra'
            print('2. Neutra - '+str(posIND2)+' - '+str(negIND2))
            
        tokens.append(classified)
        
    
    print('IND1 - % de positivas es '+str(positive_count/(positive_count+negative_count)))
    print('IND1 - % de negativas es '+str(negative_count/(positive_count+negative_count)))
    
    print('IND2 - % de positivas es '+str(positive_count2/(positive_count2+negative_count2)))
    print('IND2 - % de negativas es '+str(negative_count2/(positive_count2+negative_count2)))
    
    return(tokens)


sented = sentimentClassifier(relevant_news_filtered, 1.3, 1.15)


########################################################################
####    CHECKING RESULTS                                  ##############
########################################################################

concurso_sent = []
activa_sent = []
moroso_sent = []

for sent in sented:
    if sent['status'] is 'concurso':
        concurso_sent.append(sent)
    if sent['status'] is 'activa':
        activa_sent.append(sent)
    if sent['status'] is 'moroso':
        moroso_sent.append(sent) 

con_neg = 0
con_pos = 0
tot_neg = 0
tot_pos = 0
act_neg = 0
act_pos = 0

emp_con_neg = 0
emp_con_pos = 0
emp_tot_neg = 0
emp_tot_pos = 0

len(sented)
    
################### CONCURSO ###################

emp_con = getEmpresas(concurso_sent)
print(emp_con[0])
print(emp_con[1])

################### ACTIVA ###################

emp_act = getEmpresas(activa_sent)
print(emp_act[0])

################### ACTIVA ###################

emp_mor = getEmpresas(moroso_sent)
print(emp_mor[0])

################### CONCURSO DETALLE ###################

lista_emp_conc_neg = []
for con in concurso_sent:
    if con['sentiment'] is 'Negativa':
        con_neg +=1
        lista_emp_conc_neg.append(con)

emp_conc_neg = getEmpresas(lista_emp_conc_neg)
print(emp_conc_neg[0])

#--------------------------------------------------------

lista_emp_conc_pos = []
for con in concurso_sent:
    if con['sentiment'] is 'Postiva':
        con_pos +=1
        lista_emp_conc_pos.append(con)

lista_emp_conc_pos = [x for x in lista_emp_conc_pos if x['Empresa'] not in emp_conc_neg[1]]
emp_conc_pos = getEmpresas(lista_emp_conc_pos)
print(emp_conc_pos[0])

################### ACTIVA DETALLE ###################

lista_emp_act_neg = []
for con in activa_sent:
    if con['sentiment'] is 'Negativa':
        act_neg +=1
        lista_emp_act_neg.append(con)

emp_act_neg = getEmpresas(lista_emp_act_neg)
print(emp_act_neg[0])

#--------------------------------------------------------

lista_emp_act_pos = []
for con in activa_sent:
    if con['sentiment'] is 'Postiva':
        act_pos +=1
        lista_emp_act_pos.append(con)

lista_emp_act_pos = [x for x in lista_emp_act_pos if x['Empresa'] not in emp_act_neg[1]]
emp_act_pos = getEmpresas(lista_emp_act_pos)
print(emp_act_pos[0])

################### MOROSO DETALLE ###################

mor_neg = 0
mor_pos = 0

lista_emp_mor_neg = []
for con in moroso_sent:
    if con['sentiment'] is 'Negativa':
        mor_neg +=1
        lista_emp_mor_neg.append(con)

emp_mor_neg = getEmpresas(lista_emp_mor_neg)
print(emp_mor_neg[0])

lista_emp_mor_pos = []
for con in moroso_sent:
    if con['sentiment'] is 'Postiva':
        mor_pos +=1
        lista_emp_mor_pos.append(con)

lista_emp_mor_pos = [x for x in lista_emp_mor_pos if x['Empresa'] not in emp_mor_neg[1]]        
emp_act_pos = getEmpresas(lista_emp_mor_pos)
print(emp_act_pos[0])

################### TOTALES DETALLE ###################

lista_emp_neg = []    
for con in sented:
    if con['sentiment'] is 'Negativa':
        tot_neg +=1
        lista_emp_neg.append(con)

emp_neg = getEmpresas(lista_emp_neg)
print(emp_neg[0])     


lista_emp_pos = [] 
for con in sented:
    if con['sentiment'] is 'Postiva':
        tot_pos +=1
        lista_emp_pos.append(con)

lista_emp_pos = [x for x in lista_emp_pos if x['Empresa'] not in emp_neg[1]]  
emp_pos = getEmpresas(lista_emp_pos)
print(emp_pos[0])
       
TMR = (con_neg/tot_neg)/(con_pos/tot_pos)

TMR_emp = (emp_conc_neg[0]/emp_neg[0])/(emp_conc_pos[0]/emp_pos[0])

print(TMR)
print(TMR_emp)