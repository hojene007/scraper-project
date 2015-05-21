# -*- coding: utf-8 -*-
"""
Created on Fri May 15 10:50:24 2015

@author: bluecap
"""
import MySQLdb
import pandas as pd
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#### Conectando a baso de datos y tirando empresas con concurso
host = "bluecap.cubz34n4knn2.eu-central-1.rds.amazonaws.com"
user = "bluecap"
password = "Bluecap2005"
dbname = "einformaDB"

db = MySQLdb.connect(host, user, password, dbname)
cursor = db.cursor()

tiraMiTabla = "select *from einformaDB.bingNoticias where length(fecha)=10;" # ya no hay una tabla limpia - se contiene filas duplicadas
df_cleaned = pd.read_sql(tiraMiTabla, db)

# Tenemos que limpiar dfAll para alcanzar solo fechas en columna de fechas
dfNew = pd.DataFrame()
dfNew = dfNew.append(dfAll.iloc[0, :])
temp = pd.DataFrame()
for i in range(1, dfAll.shape[0]) :
    fecha = dfAll.iloc[i, 1]
    if "hour" in fecha  :
        print "removando fila con string %s " % fecha
    else :
        a = temp.append(dfAll.iloc[i, :])
        dfNew = pd.concat([dfNew, a], axis=0)
        print "fila numero %s " % i
        
# VERIFICA EL NOMBRE DE LA TABLA !!!!!!!!!!!!!!!!!!!!!!
dropIfthere = "DROP TABLE IF EXISTS einformaDB.bingNoticias2;"
nuevaTabla = """CREATE TABLE einformaDB.bingNoticias2
(
empresa text,
fecha datetime,
autor text,
link text, 
parrafo text, 
titulo text
);"""
cursor.execute(dropIfthere)
cursor.execute(nuevaTabla)

# VERIFICA EL NOMBRE DE LA TABLA !!!!!!!!!!!!!!!!!!!!!!
insertString = "INSERT INTO einformaDB.bingNoticias2 (empresa, fecha, autor, link, parrafo, titulo)  values (%s, %s, %s, %s, %s, %s);"


for i in range(0, dfAll.shape[0]):
    cursor.execute(insertString, (dfAll.iloc[i, 0], dfAll.iloc[i, 1], dfAll.iloc[i, 2], dfAll.iloc[i, 3], dfAll.iloc[i, 4], dfAll.iloc[i, 5])) 
    db.commit()
    print i
    

##################################

""" Busqueda de noticias relevantos basado al fecha de concurso"""
#################################

#nombres_fechas < ya tenemos
## un funcion para colegir los datos de la noticia en un formato que se puede compararse con nombres_fechas
##



    