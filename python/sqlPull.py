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
     
host = "bluecap.cubz34n4knn2.eu-central-1.rds.amazonaws.com"
user = "bluecap"
password = "Bluecap2005"
dbname = "einformaDB"

db = MySQLdb.connect(host, user, password, dbname)
cursor = db.cursor()

#### get first few rows
# query1 = "select*from einformaDB.eInforma_Empresas limit 5;"
# top5= cursor.execute(query1)

queryConcurso = "SELECT * FROM einformaDB.Empresas where situacion like '%Concurso%'and situacion like '%CONCURSO%' ;"

df = pd.read_sql(queryConcurso, db)
nombres = list(df['nombre_empresa'])


###################################
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
queryNoticias = "SELECT * FROM einformaDB.PeriodicosGrandes4 group by link;"
noticiasDF = pd.read_sql(queryNoticias, db)

type(noticiasDF.iloc[0, 2])
fechas_de_noticias = [datetime.strptime(a , '%d/%m/%Y') for a in noticiasDF["fecha"]]
noticiasDF["fecha_d_noticia_limp"] = pd.DataFrame(fechas_de_noticias)

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
    
new_noticias_df =construirVecFechas(nombres_fechas, noticiasDF)        

## Solo donde fecha_concurso > fecha_noticia
new_noticias_df["fecha"] = pd.to_datetime(new_noticias_df["fecha"])
new_noticias_df["fecha_de_concurso_de_empresa"] = pd.to_datetime(new_noticias_df["fecha_de_concurso_de_empresa"])


############### Hasta aqui para text_mining1.py ################################################################

articulos_relevantes = new_noticias_df[new_noticias_df["fecha"] < new_noticias_df["fecha_de_concurso_de_empresa"]]
articulos_relevantes["difer_fechas"] = articulos_relevantes["fecha_de_concurso_de_empresa"] - articulos_relevantes["fecha"]

max_diferencia = datetime.timedelta(days=365)

articulos_relevantes2 = articulos_relevantes[articulos_relevantes["difer_fechas"]<max_diferencia]

tablaDeTexto = """CREATE TABLE einformaDB.tablaDeTexto
(
fuenta text,
empresa text,
fecha datetime,
autor text,
link text, 
parrafo text, 
titulo text, 
texto text, 
fecha_concurso datetime, 
dif_fechas text
);"""
cursor.execute(tablaDeTexto)
pd.io.sql.write_frame(articulos_relevantes2, "einformaDB.tablaDeTexto2", db, flavor='mysql', if_exists='replace')

empresasUnicos = pd.DataFrame(articulos_relevantes["empresa"].unique())
articulos_relevantes2.iloc[5, 1]
articulos_relevantes2.iloc[5, 7].decode("utf-8")


#############################
""" arreglando links con archivo. ... no se funcionan bien ahora"""
#############################
dictElMundoN = {}
dictElPaisN = {}
dictExpansionN = {}

queryNoticias = "SELECT * FROM einformaDB.PeriodicosGrandes4 group by link;"
df = pd.read_sql(queryNoticias, db)

for empr in dictElMundo :
    dictElMundoN[empr] = dictElMundo[empr]
    if len(dictElMundo[empr]) > 0 :
        for link in dictElMundo[empr] :
            link = dictElMundo[empr]["link"]
            textToReplace = tiraElMundo(link)
            dictElMundoN[empr]["texto"] = textToReplace
            
maxL = 0
for empr in dictExpansion :
    length = len(dictExpansion[empr]) 
    if maxL < length :
        maxL = length
print maxL            