# -*- coding: utf-8 -*-
"""
Created on Tue May 12 09:56:57 2015

@author: bluecap
se usa Noticias.py para recolectar articulos mientras consiguiendo codigo en Noticias.py - tienes que correr los funciones por dentrolo anterior que corriendo estas aquí 
"""

import pymysql
import pymysql.cursors
import string
#import os
import time
import pandas as pd
import periodicos_class_bs4 as news_getter
from pymongo import MongoClient
import json

client = MongoClient()
db = client.social_hats

wait = 0

badTerms = ["SL", "SA", "S.L.", "SOCIEDAD", "ANONIMA", "LIMITADA", "SCCL", "LIMITADA.", "S.A.", "S.C.C.L.", "SOCIETAT", "S.A", "S A", "SCP", "SLP", "SLL"]

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

'''
### Conectando a baso de datos y tirando empresas con concurso
host = "bluecap.cubz34n4knn2.eu-central-1.rds.amazonaws.com"
user = "bluecap"
password = "Bluecap2005"
dbname = "einformaDB"#

# Connect to the database
connection = pymysql.connect(host=host,
                             user=user,
                             passwd=password,
                             db=dbname,
                             port=3306)
#with connection.cursor() as cursor:

cursor = connection.cursor()
#db.concurso.drop()

queryConcurso = "SELECT * FROM einformaDB.Empresas where situacion like '%Concurso%' and situacion like '%CONCURSO%';"
nombres_fechas = pd.DataFrame()
dfAll = pd.read_sql(queryConcurso, connection)
records = json.loads(dfAll.T.to_json()).values()
db.concurso.insert(records)
'''
nombres_fechas = pd.DataFrame()
dfAll = pd.DataFrame(list(db.concurso.find()))
nombres_fechas[['nombre_empresa', 'situacion']] = dfAll[['nombre_empresa', 'situacion']]
nombresNuevos = nombresLimpiador(nombresLimpiador(list(nombres_fechas['nombre_empresa']), badTerms), badTerms)
nombres_fechas[['nom_limpios']] = pd.DataFrame(nombresNuevos)
fechasALimpiar = list(nombres_fechas['situacion'])
fechas = [a[a.index(":") + 1:a.rindex(")")] for a in fechasALimpiar]
fechas =[a[1:] for a in fechas]
nombres_fechas[['fecha_concurso']] = pd.DataFrame(fechas)
nombres_fechas = nombres_fechas[['nom_limpios', 'fecha_concurso','situacion']]
nombres_fechas[['situacion']] = pd.DataFrame(['Concurso' for a in list(nombres_fechas['situacion']) if 'Concurso' in a])
'''
queryConcurso_2 = "SELECT * FROM einformaDB.Empresas where situacion = 'Activa' LIMIT 25000;"
dfAll2 = pd.read_sql(queryConcurso_2, connection)
records = json.loads(dfAll2.T.to_json()).values()
db.activas.insert(records)
'''
nombres_fechas_act = pd.DataFrame()
dfAll2 = pd.DataFrame(list(db.activas.find()))
nombres_fechas_act[['nombre_empresa', 'situacion']] = dfAll2[['nombre_empresa', 'situacion']]
nombresNuevos2 = nombresLimpiador(nombresLimpiador(list(nombres_fechas_act['nombre_empresa']), badTerms), badTerms)
nombres_fechas_act[['nom_limpios']] = pd.DataFrame(nombresNuevos2)
fechasALimpiar2 = list(nombres_fechas_act['situacion'])
fechas2 = ['01/01/2016' for a in fechasALimpiar2]
nombres_fechas_act[['fecha_concurso']] = pd.DataFrame(fechas2) 
nombres_fechas_act['nombre_empresa'] = nombres_fechas_act['nom_limpios']
nombres_fechas_act = nombres_fechas_act[['nom_limpios', 'fecha_concurso', 'situacion']]

db2 = client.empresas_morosas
morosos = db2.antoni.find()
moroso_nombre = []
for moroso in morosos:
    moroso_nombre.append(moroso['Denominación:'])

moroso_ok = []
for moroso in moroso_nombre:
    if '(' in moroso:
        befor_keyowrd, keyword, after_keyword = moroso.partition('(')
        moroso_ok.append(befor_keyowrd.strip())
    else:
        moroso_ok.append(moroso)
        
moroso_ok = nombresLimpiador(nombresLimpiador(moroso_ok, badTerms), badTerms)

frames = [nombres_fechas, nombres_fechas_act]

nombres_fechas = pd.concat(frames)


if __name__ == '__main__':
    
    dictElPais = {}
    dictElMundo = {}
    dictExpansion = {}
    
    paraActualisarExpansion = {}
    paraActualisarElMundo = {}
    paraActualisarElPais = {} # un diccionario temporario
    
    noms = list(nombres_fechas['nom_limpios'])
    [noms.append(a) for a in moroso_ok]
    ind = 115
    cadaN_updateDB = 1000
    N = len(noms)
    indexError = 0
    
    try :
        for i,nom in enumerate(noms) :
            # para bigNoticias3 acabadó a 280
            cursor = db.noticias.find({"Empresa": nom})
            print('----------------- Empresa '+str(i)+' / '+str(N)+' ('+"{0:.0f}%".format(float(i)/N* 100)+') --------------')
            if cursor.count()==0:
                if noms.index(nom) > -1:
                        ind= noms.index(nom)
                        try :
                            expansionTemp = []
                            expansionTemp = news_getter.ExpansionPull(nom)
                        except :
                            print('No he podido recoger los datos de Expansion')
                        try :
                            elmundoTemp = []
                            elmundoTemp = news_getter.ElMundoPull(nom)
                        except :
                            print('No he podido recoger los datos de El Mundo')
                        try :
                            elpaisTemp = []
                            elpaisTemp = news_getter.ElPaisPull(nom)
                        except :
                            print('No he podido recoger los datos de El Pais') 
                        
                        if expansionTemp or elmundoTemp or elpaisTemp:
                        
                            [db.noticias.insert_one(a) for a in expansionTemp]
                            [db.noticias.insert_one(a) for a in elmundoTemp]
                            [db.noticias.insert_one(a) for a in elpaisTemp]
                        
                            dictExpansion[nom] = expansionTemp
                            dictElMundo[nom] = elmundoTemp
                            dictElPais[nom] = elpaisTemp
                        
                        else:
                            db.noticias.insert_one({"Empresa": nom})
                            
                        '''
                        paraActualisarExpansion[nom] = expansionTemp
                        paraActualisarElMundo[nom] = elmundoTemp
                        paraActualisarElPais[nom] = elpaisTemp
                        
                        #print("he terminado yendo a yahoo para sacar info sobre empresa # %s de %s " % (ind, N))
                        if ind >0 and ind%cadaN_updateDB==0 :
                            try :
                                updateDBPeriodicosGrandes2("expansion", paraActualisarExpansion, insertString)
                                updateDBPeriodicosGrandes2("elmundo", paraActualisarElMundo, insertString)
                                updateDBPeriodicosGrandes2("elpais", paraActualisarElPais, insertString)
                            except :
                                # Connect to the database
                                connection = pymysql.connect(host=host,
                                                             user=user,
                                                             passwd=password,
                                                             db=dbname,
                                                             port=3306)
                                #with connection.cursor() as cursor:
                                cursor = connection.cursor()
                                updateDBPeriodicosGrandes2("expansion", paraActualisarExpansion, insertString)
                                updateDBPeriodicosGrandes2("elmundo", paraActualisarElMundo, insertString)
                                updateDBPeriodicosGrandes2("elpais", paraActualisarElPais, insertString)
                                
                            paraActualisarExpansion = {}
                            paraActualisarElMundo = {}
                            paraActualisarElPais = {}
                        '''
            else:
                try:
                    print(str(nom)+' ya está en la base de datos')
                except:
                    continue

        time.sleep(wait)
        
    except KeyboardInterrupt : 
        print("Master says stop!")
    finally:
        connection.close()